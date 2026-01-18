import UIKit
import AVFoundation

class ViewController: UIViewController, CameraManagerDelegate, ESP32ManagerDelegate {

    // UI Elements (Programmatic or Storyboard)
    var statusLabel: UILabel!
    var settingsButton: UIButton!
    
    let cameraManager = CameraManager()
    let espManager = ESP32Manager.shared
    let audioManager = SheldonAudioManager()
    
    // Random Event Timer
    var randomTimer: Timer?

    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
        
        // Delegates
        cameraManager.delegate = self
        espManager.delegate = self
        
        // Start Camera
        cameraManager.setupCamera(in: self.view)
        
        // Start Random Events (30s interval for "stuck" or "random" fun)
        randomTimer = Timer.scheduledTimer(withTimeInterval: 30.0, repeats: true) { [weak self] _ in
            self?.triggerRandomEvent()
        }
    }
    
    override func viewDidLayoutSubviews() {
        super.viewDidLayoutSubviews()
        cameraManager.updatePreviewFrame(self.view.bounds)
    }

    func setupUI() {
        self.view.backgroundColor = .black
        
        // 1. Status Label (Overlay)
        statusLabel = UILabel()
        statusLabel.translatesAutoresizingMaskIntoConstraints = false
        statusLabel.text = "Waiting for Camera..."
        statusLabel.textColor = .white
        statusLabel.font = UIFont.systemFont(ofSize: 18, weight: .bold)
        statusLabel.backgroundColor = UIColor(white: 0, alpha: 0.6)
        statusLabel.textAlignment = .center
        statusLabel.layer.cornerRadius = 10
        statusLabel.layer.masksToBounds = true
        
        self.view.addSubview(statusLabel)
        
        // 2. Settings / IP Button
        settingsButton = UIButton(type: .system)
        settingsButton.translatesAutoresizingMaskIntoConstraints = false
        settingsButton.setTitle("Configure IP", for: .normal)
        settingsButton.addTarget(self, action: #selector(tappedSettings), for: .touchUpInside)
        settingsButton.backgroundColor = UIColor(white: 0, alpha: 0.6)
        settingsButton.layer.cornerRadius = 8
        settingsButton.setTitleColor(.cyan, for: .normal)
        
        self.view.addSubview(settingsButton)
        
        // Constraints
        NSLayoutConstraint.activate([
            statusLabel.topAnchor.constraint(equalTo: self.view.safeAreaLayoutGuide.topAnchor, constant: 20),
            statusLabel.centerXAnchor.constraint(equalTo: self.view.centerXAnchor),
            statusLabel.widthAnchor.constraint(greaterThanOrEqualToConstant: 200),
            statusLabel.heightAnchor.constraint(greaterThanOrEqualToConstant: 40),
            
            settingsButton.bottomAnchor.constraint(equalTo: self.view.safeAreaLayoutGuide.bottomAnchor, constant: -20),
            settingsButton.centerXAnchor.constraint(equalTo: self.view.centerXAnchor)
        ])
    }
    
    @objc func tappedSettings() {
        let alert = UIAlertController(title: "Settings", message: "Enter ESP32 IP Address", preferredStyle: .alert)
        alert.addTextField { tf in
            tf.text = self.espManager.ipAddress
            tf.keyboardType = .numbersAndPunctuation
        }
        alert.addAction(UIAlertAction(title: "Save", style: .default, handler: { _ in
            if let ip = alert.textFields?.first?.text, !ip.isEmpty {
                self.espManager.ipAddress = ip
                self.showStatus("IP Updated: \(ip)")
            }
        }))
        alert.addAction(UIAlertAction(title: "Cancel", style: .cancel))
        present(alert, animated: true)
    }
    
    // MARK: - Logic
    
    func triggerRandomEvent() {
        // 20% chance to send "random" event
        if Int.random(in: 0...100) < 20 {
            let type = "random"
            showStatus("🎲 Random Event")
            espManager.sendManualEvent(event: type) // POST (Bypasses cooldown)
            audioManager.playEvent(type)
            flashScreen()
        }
    }
    
    // For Camera Detections (GET /detect)
    func handleDetection(type: String, label: String) {
        showStatus("Detecting: \(type.uppercased())")
        espManager.sendDetectionEvent(type: type)
        audioManager.playEvent(type) 
        flashScreen()
    }

    func flashScreen() {
        let flash = UIView(frame: self.view.bounds)
        flash.backgroundColor = .white
        flash.alpha = 0.3
        self.view.addSubview(flash)
        UIView.animate(withDuration: 0.2) {
            flash.alpha = 0.0
        } completion: { _ in
            flash.removeFromSuperview()
        }
    }
    
    func showStatus(_ text: String) {
        DispatchQueue.main.async {
            self.statusLabel.text = " \(text) "
        }
    }

    // MARK: - CameraManagerDelegate
    
    func didDetect(type: String, confidence: Float, bounds: CGRect) {
        print("Detected: \(type) (\(confidence))")
        
        // Convert internal type to display text
        let displayText: String
        switch type {
        case "saw_human": displayText = "👤 HUMAN SAW"
        case "collision": displayText = "🛑 OBSTACLE AHEAD"
        default: displayText = type
        }
        
        handleDetection(type: type, label: displayText)
    }
    
    func cameraSetupFailed(error: String) {
        showStatus("Error: \(error)")
    }
    
    // MARK: - ESP32ManagerDelegate
    
    func didSendDetection(type: String, success: Bool) {
        if success {
            showStatus("Sent: \(type) ✅")
            // Clear status after 2s
            DispatchQueue.main.asyncAfter(deadline: .now() + 2.0) {
                self.statusLabel.text = "Scanning..."
            }
        } else {
            showStatus("Failed sending \(type) ❌")
        }
    }
}
