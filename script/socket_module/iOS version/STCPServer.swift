//
//  STCPServer.swift
//  Socket test
//
//  Created by hanyi02 on 2020/2/2.
//  Copyright © 2020 Stan. All rights reserved.
//

import Foundation
import Network


class STCPServer {
    
    let port: NWEndpoint.Port
    let listener: NWListener
    var clients: [UInt16:Messenger]
    
    var current_id: UInt16
    
    var ready_callback: ((UInt16) -> Void)?
    var new_client_callback: ((Messenger) -> Void)?
    var recv_callback: ((Messenger) -> Void)?
    var send_callback: ((Messenger) -> Void)?
    var client_ready_callback: ((Messenger) -> Void)?
    var client_close_callback: ((Messenger, Error?) -> Void)?
    var close_callback: (() -> Void)?
    
    init(_ port: UInt16) {
        self.port = NWEndpoint.Port(rawValue: port)!
        self.listener = try! NWListener(using: .tcp, on: self.port)
        self.clients = [:]
        self.current_id = 0
    }
    
    func start() {
        self.listener.stateUpdateHandler = self.state_change(to: )
        self.listener.newConnectionHandler = self.accept(new_connection: )
        self.listener.start(queue: .main)
    }
    
    func state_change(to newState: NWListener.State)
    {
        switch newState {
        case .ready:
            if let callback = self.ready_callback {
                callback(self.port.rawValue)
            }
        case .failed(_):
            self.close()
        case .cancelled:
            print("cancelled")
            break
        case .waiting(_):
            print("waiting")
            break
        default:
            break
        }
    }
    

    
    func accept(new_connection: NWConnection)
    {
        let client = Messenger(connection: new_connection, id: self.current_id)
        current_id += 1
        self.clients[client.ID] = client
        client.recv_callback = self.recv_callback
        client.send_callback = self.send_callback
        client.ready_callback = self.client_ready_callback
        client.close_callback = self.client_close_callback
        
        client.start()
        
        if let callback = self.new_client_callback {
            callback(client)
        }
    }
    
    func close() {
        self.listener.stateUpdateHandler = nil
        self.listener.newConnectionHandler = nil
        self.listener.cancel()
        for (_, client) in self.clients {
            client.ready_callback = nil
            client.recv_callback = nil
            client.close_callback = nil
            client.send_callback = nil
            client.close(error: nil)
        }
        self.clients.removeAll()
        self.current_id = 0
        
        self.ready_callback = nil
        self.new_client_callback = nil
        self.recv_callback = nil
        self.client_close_callback = nil
        self.send_callback = nil
        self.client_ready_callback = nil
        
        if let callback = self.close_callback {
            self.close_callback = nil
            callback()
        }
    }

}
