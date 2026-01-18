import AVFoundation
import Foundation
import Combine

// A. Struct to handle the Audio Map
// A. Struct to handle the Audio Map
struct AudioMap: Codable, Sendable {
    let BOOT: [String]?
    let SAW_HUMAN: [String]?
    let COLLISION: [String]?
    let RANDOM: [String]?
    let STUCK: [String]?
}

class SheldonAudioManager: ObservableObject {
    private var player: AVPlayer?
    private var audioMap: AudioMap?
    private let baseURL = "http://192.168.4.1"
    
    init() {
        fetchAudioMap()
        setupSession()
    }
    
    // 1. Setup Audio Session
    private func setupSession() {
        do {
            try AVAudioSession.sharedInstance().setCategory(.playback, mode: .default, options: [.mixWithOthers])
            try AVAudioSession.sharedInstance().setActive(true)
        } catch {
            print("Audio Session Error: \(error)")
        }
    }
    
    // 2. Fetch the Map on startup
    func fetchAudioMap() {
        guard let url = URL(string: "\(baseURL)/audio_map.json") else { return }
        
        URLSession.shared.dataTask(with: url) { [weak self] data, _, error in
            guard let self = self else { return }
            
            if let data = data {
                do {
                    // Decode off-main-thread is fine if AudioMap is Sendable
                    let decodedMap = try JSONDecoder().decode(AudioMap.self, from: data)
                    // Update state on Main Actor to be safe
                    DispatchQueue.main.async {
                        self.audioMap = decodedMap
                        print("✅ Audio Map Loaded!")
                    }
                } catch {
                    print("JSON Decode Error: \(error)")
                }
            } else if let error = error {
                print("Fetch Error: \(error.localizedDescription)")
            }
        }.resume()
    }
    
    // 3. Play Audio by Category
    func playEvent(_ event: String) {
        guard let map = audioMap else {
            print("Audio Map not loaded yet.")
            return
        }
        
        var files: [String]?
        
        // Normalize event string to Uppercase to match Struct properties
        let key = event.uppercased()
        
        switch key {
        case "SAW_HUMAN": files = map.SAW_HUMAN
        case "COLLISION": files = map.COLLISION
        case "STUCK": files = map.STUCK
        case "RANDOM": files = map.RANDOM
        case "BOOT": files = map.BOOT
        default: files = map.RANDOM
        }
        
        guard let validFiles = files, !validFiles.isEmpty else {
            print("No audio files found for \(key)")
            return
        }
        
        // Pick Random File
        let randomFile = validFiles.randomElement()!
        
        // Construct Path. Assumes structure: /CATEGORY/filename.mp3
        // If the map just has filenames, we might need to append category path.
        // Assuming map values are full filenames relative to root or inside a folder.
        // Based on user prompt: "GET /CATEGORY/filename.mp3"
        // So we presume the map just gives the filename, and we construct the path.
        
        // Safety: If filename already has slashes, handle it?
        // Let's stick to the prompt's constructed path style:
        let fullPath = "\(baseURL)/\(key)/\(randomFile)"
        
        // Escape spaces if needed
        guard let encodedPath = fullPath.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) else { return }
        
        print("🔊 Playing: \(encodedPath)")
        playUrl(encodedPath)
    }
    
    private func playUrl(_ urlString: String) {
        guard let url = URL(string: urlString) else { return }
        let item = AVPlayerItem(url: url)
        
        // Create player
        self.player = AVPlayer(playerItem: item)
        self.player?.play()
    }
}
