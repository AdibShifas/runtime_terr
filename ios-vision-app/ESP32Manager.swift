import Foundation

protocol ESP32ManagerDelegate: AnyObject {
    func didSendDetection(type: String, success: Bool)
}

class ESP32Manager {
    static let shared = ESP32Manager()
    weak var delegate: ESP32ManagerDelegate?
    
    // Config
    var ipAddress: String = "192.168.4.1"
    var port: String = "80"
    
    private let session: URLSession
    
    init(timeout: TimeInterval = 2.0) {
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = timeout
        config.timeoutIntervalForResource = timeout
        self.session = URLSession(configuration: config)
    }
    
    // 1. Auto-Detection (Camera) - GET /detect
    func sendDetectionEvent(type: String) {
        // API Guide: GET /detect?type=saw_human
        guard let url = URL(string: "http://\(ipAddress):\(port)/detect?type=\(type)") else { return }
        print("[ESP32] Detecting: \(type) -> \(url.absoluteString)")
        
        let task = session.dataTask(with: url) { [weak self] _, response, error in
            let success = (error == nil && (response as? HTTPURLResponse)?.statusCode == 200)
            DispatchQueue.main.async {
                self?.delegate?.didSendDetection(type: type, success: success)
            }
        }
        task.resume()
    }
    
    // 2. Manual Audio Triggers - POST /event
    func sendManualEvent(event: String) {
        let body: [String: String] = ["event": event]
        sendPostRequest(path: "/event", body: body)
    }
    
    // 3. Mode Switching - POST /mode
    func setMode(drive: String, voice: String) {
        let body: [String: String] = ["drive": drive, "voice": voice]
        sendPostRequest(path: "/mode", body: body)
    }
    
    // 4. Joystick Control - POST /move
    func sendJoystick(x: Int, y: Int) {
        let body: [String: Int] = ["x": x, "y": y]
        sendPostRequest(path: "/move", body: body)
    }
    
    // Helper for POST
    private func sendPostRequest(path: String, body: Any) {
        guard let url = URL(string: "http://\(ipAddress):\(port)\(path)") else { return }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: body, options: [])
        } catch {
            print("[ESP32] JSON Serialization Error: \(error)")
            return
        }
        
        // Fire and Forget (mostly)
        session.dataTask(with: request) { _, response, error in
            if let error = error {
                print("[ESP32] POST Error (\(path)): \(error.localizedDescription)")
            }
        }.resume()
    }
}
