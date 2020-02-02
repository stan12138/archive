//
//  ViewController.swift
//  Socket test
//
//  Created by hanyi02 on 2020/1/29.
//  Copyright © 2020 Stan. All rights reserved.
//

import UIKit
import Network

class ViewController: UIViewController {

    var reocrd: [Messenger] = []
    
    var Server: STCPServer?
    
    var port: UInt16 = 5000
    
    override func viewDidLoad() {
        super.viewDidLoad()
                
        self.Server = STCPServer(self.port)
        self.setup_server_handler()
        self.Server?.start()

    }
    
    func server_close() {
        print("server begin fail")
        self.port += 1
        self.Server = STCPServer(self.port)
        self.setup_server_handler()
        self.Server?.start()
    }
    
    func setup_server_handler() {
        self.Server!.ready_callback = self.server_ready(port: )
        self.Server!.new_client_callback = self.get_client(client: )
        self.Server!.recv_callback = self.recv_data(client: )
        self.Server!.client_ready_callback = self.client_ready(client: )
        self.Server!.client_close_callback = self.client_close
        self.Server!.close_callback = self.server_close
    }
    
    func server_ready(port: UInt16) {
        print("server ready in \(port)")
    }
    
    func get_client(client: Messenger) {
        print("get a client: \(client.ID)")
    }
    
    func recv_data(client: Messenger) {
        print(client.header, String(data: client.body, encoding: .utf8)!)
        client.send(header: client.header, body: client.body)
    }
    
    func client_ready(client: Messenger) {
        print("client ready: \(client.ID)")
    }
    
    func client_close(client: Messenger, error: Error?) {
        print("client close: \(client.ID)")
    }

}

