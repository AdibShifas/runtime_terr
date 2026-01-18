import UIKit
import AVFoundation
import Vision

protocol CameraManagerDelegate: AnyObject {
    func didDetect(type: String, confidence: Float, bounds: CGRect)
    func cameraSetupFailed(error: String)
}

class CameraManager: NSObject, AVCaptureVideoDataOutputSampleBufferDelegate {
    
    weak var delegate: CameraManagerDelegate?
    
    private let captureSession = AVCaptureSession()
    private var videoOutput = AVCaptureVideoDataOutput()
    // Cooldown Logic
    private var lastDetectionTimes: [String: Date] = [:]
    private var lastFrameProcessTime: Date = Date.distantPast
    
    var previewLayer: AVCaptureVideoPreviewLayer?
    
    override init() {
        super.init()
        // Vision setup is done per-frame in captureOutput to allow specific handlers
    }
    
    func setupCamera(in view: UIView) {
        captureSession.sessionPreset = .medium // Save battery
        
        guard let device = AVCaptureDevice.default(.builtInWideAngleCamera, for: .video, position: .back),
              let input = try? AVCaptureDeviceInput(device: device) else {
            delegate?.cameraSetupFailed(error: "No camera found")
            return
        }
        
        if captureSession.canAddInput(input) {
            captureSession.addInput(input)
        }
        
        // Output setup
        videoOutput.videoSettings = [kCVPixelBufferPixelFormatTypeKey as String: Int(kCVPixelFormatType_32BGRA)]
        videoOutput.setSampleBufferDelegate(self, queue: DispatchQueue(label: "cameraQueue"))
        
        if captureSession.canAddOutput(videoOutput) {
            captureSession.addOutput(videoOutput)
        }
        
        // Preview Layer
        previewLayer = AVCaptureVideoPreviewLayer(session: captureSession)
        previewLayer?.videoGravity = .resizeAspectFill
        previewLayer?.frame = view.bounds
        if let layer = previewLayer {
            view.layer.insertSublayer(layer, at: 0)
        }
        
        // Background thread start
        DispatchQueue.global(qos: .userInitiated).async { [weak self] in
            self?.captureSession.startRunning()
        }
    }

    // Capture Output Delegate
    func captureOutput(_ output: AVCaptureOutput, didOutput sampleBuffer: CMSampleBuffer, from connection: AVCaptureConnection) {
        // 1. GLOBAL CPU SAVER: Don't process every single frame (30fps -> 2fps)
        // This saves battery but doesn't handle the "Event Logic" cooldown.
        if Date().timeIntervalSince(lastFrameProcessTime) < 0.5 {
            return
        }
        lastFrameProcessTime = Date()

        guard let pixelBuffer = CMSampleBufferGetImageBuffer(sampleBuffer) else { return }
        
        let imageRequestHandler = VNImageRequestHandler(cvPixelBuffer: pixelBuffer, orientation: .right, options: [:])
        
        do {
            // Processing logic needs to be specialized here.
            
            let humanReq = VNDetectHumanRectanglesRequest { [weak self] req, err in
                self?.processHuman(req, err)
            }
            // Optimize for speed
            humanReq.upperBodyOnly = false
            
            let rectReq = VNDetectRectanglesRequest { [weak self] req, err in
                self?.processSimpleRect(req, err)
            }
            rectReq.minimumConfidence = 0.8
            rectReq.minimumSize = 0.4 // Only detect BIG things (>40% of screen approx)
            
            try imageRequestHandler.perform([humanReq, rectReq])
            
        } catch {
            print(error)
        }
    }
    
    func processHuman(_ request: VNRequest, _ error: Error?) {
        guard let results = request.results as? [VNHumanObservation], !results.isEmpty else { return }
        
        // Just take the biggest/first one
        if let first = results.first {
            notifyDetection(type: "saw_human", confidence: first.confidence, bounds: first.boundingBox)
        }
    }
    
    func processSimpleRect(_ request: VNRequest, _ error: Error?) {
        guard let results = request.results as? [VNRectangleObservation], !results.isEmpty else { return }
        
        // User Requirement: "Trigger when object takes >50% of frame"
        // boundingBox area = w * h
        if let first = results.sorted(by: { ($0.boundingBox.width * $0.boundingBox.height) > ($1.boundingBox.width * $1.boundingBox.height) }).first {
            let area = first.boundingBox.width * first.boundingBox.height
            
            // 0.5 is 50%
            if area > 0.5 {
                 notifyDetection(type: "collision", confidence: first.confidence, bounds: first.boundingBox)
            }
        }
    }
    
    private func notifyDetection(type: String, confidence: Float, bounds: CGRect) {
        // 2. LOGIC COOLDOWN: Prevent spamming specific events
        // Default to 5.0 seconds for humans, 2.0 for others
        let requiredCooldown: TimeInterval = (type == "saw_human") ? 5.0 : 2.0
        
        if let lastTime = lastDetectionTimes[type] {
            if Date().timeIntervalSince(lastTime) < requiredCooldown {
                return // Ignored (Cooling down)
            }
        }
        
        // Update time for this specific event type
        lastDetectionTimes[type] = Date()
        
        DispatchQueue.main.async { [weak self] in
            self?.delegate?.didDetect(type: type, confidence: confidence, bounds: bounds)
        }
    }
    
    func updatePreviewFrame(_ frame: CGRect) {
        previewLayer?.frame = frame
    }
}
