//
//  Messenger.swift
//  Socket test
//
//  Created by hanyi02 on 2020/1/31.
//  Copyright © 2020 Stan. All rights reserved.
//

import Foundation
import Network

enum MessengerStatus {
    case prefix, header, body
}


class Messenger {
    let  connection: NWConnection
    
    var close_callback: ((Messenger, Error?) -> Void)? = nil
    var ready_callback: ((Messenger) -> Void)? = nil
    var recv_callback: ((Messenger) -> Void)? = nil
    var send_callback: ((Messenger) -> Void)? = nil

    var header_length: UInt16 = 0
    var body_length: Int = 0
    
    var header: [String: String] = [:]
    var body: Data = Data()
    
    var status: MessengerStatus = .prefix
    
    var data: Data = Data()
    
    var recv_done: Bool = false
    
    let ID: UInt16
    
    init(connection: NWConnection, id: UInt16) {
        self.connection = connection
        self.status = .prefix
        self.ID = id
    }
    
    func start() {
        self.connection.stateUpdateHandler = self.state_change(to: )
        self.connection.receive(minimumIncompleteLength: 1, maximumLength: 65536, completion: self.recv_handler)
        self.connection.start(queue: .main)
    }
    
    func state_change(to state: NWConnection.State) {
        switch state {
        case .waiting(let error):
            self.close(error: error)
        case .ready:
            self.ready()
        case .failed(let error):
            self.close(error: error)
        default:
            break
        }
    }
    
    func send(header: [String:String] = [:], body: Data = Data()) {
        var new_header = header
        new_header["CL"] = String(body.count)
        var message = self.construct_header(header: new_header)
        message += body
        self.connection.send(content: message, completion: .contentProcessed(self.send_done(error: )))
    }
    
    func send_done(error: Error?) {
        if let error=error {
            self.close(error: error)
        }
        if self.send_callback != nil {
            self.send_callback!(self)
        }
    }
    
    func construct_header(header: [String:String]) -> Data {
        var me: String = ""
        for (name, value) in header {
            me += name + ":" + value + ";"
        }
        me.removeLast()
        
        let h = Data(me.utf8)
        let s: UInt16 = UInt16(h.count)
        return UInt162dada(s)+h
    }
    
    func recv_handler(data: Data?, context: NWConnection.ContentContext?, complete_flag: Bool, error: Error?) {
        if let data = data, !data.isEmpty {
            self.parse_data(data: data)
        }
        
        if complete_flag {
            self.close(error: error)
        }
        else if let error = error {
            self.close(error: error)
        }
        else {
//            print("setup recive again")
            self.connection.receive(minimumIncompleteLength: 1, maximumLength: 65536, completion: self.recv_handler)
        }
        
    }
    
    func UInt162dada(_ value: UInt16) -> Data {
        var b = value.littleEndian
        
        let s = Data(bytes: &b, count: MemoryLayout<UInt16>.size)
        
        return s
    }
    
    func Data2UInt16(_ data: Data) -> UInt16 {
        return UInt16(UInt16(data[1])<<8 + UInt16(data[0]))
    }
    
    func parse_data(data: Data) {
//        print("parse begin......")
        self.recv_done = false
        self.data.append(data)
        
        if self.status == .prefix {
            self.parse_prefix()
        }
        if self.status == .header {
            self.parse_header()
        }
        if self.status == .body {
            self.parse_body()
        }
        
        if self.recv_done {
            if self.recv_callback != nil {
                self.recv_callback!(self)
            }
        }
//        print("parse done!!!!")
    }
    
    func parse_prefix() {
        if self.data.count >= 2{
            let d = self.data[..<2]
            self.data = self.data[2...]
            self.header_length = Data2UInt16(d)
//            print(self.header_length)
            self.status = .header
        }
        else {
            self.status = .prefix
        }
    }
    
    func parse_header() {
        if self.data.count >= self.header_length {
            // 不知道为什么对于Data使用索引截取片段总是会短两个字节，但是自playground里面就可以呀？？？？？
//            print(self.header_length, self.data.prefix(Int(self.header_length)).count, self.data.count)
//            print(String(data: self.data, encoding: .utf8)!)
            let d = String(data: self.data.prefix(Int(self.header_length)), encoding: .utf8)
//            let d = String(data: self.data.subdata(in: R), encoding: .utf8)
//            print(d!)
//            self.data = self.data.suffix(from: Int(self.header_length))
            self.data = self.data.dropFirst(Int(self.header_length))
//            print(String(data: self.data, encoding: .utf8)!)
            let s1 = d!.split(separator: ";")
            self.header = [:]
            for item in s1 {
                let s2 = item.split(separator: ":")
                self.header[String(s2[0])] = String(s2[1])
            }
//            print(self.header)
            let length = Int(self.header["CL"] ?? "0")
            if let body_length = length {
                if body_length>0 {
                    self.status = .body
                    self.body_length = body_length
                }
                else {
                    self.status = .prefix
                    self.recv_done = true
                    self.body_length = 0
                    self.data = Data()
                }
            }
            else {
                self.data = Data()
                self.recv_done = true
                self.body_length = 0
                self.status = .prefix
            }
        }
        else {
            self.status = .header
        }

    }
    
    func parse_body() {
        if self.data.count < self.body_length {
            self.status = .body
        }
        else {
//            print(String(data: self.data, encoding: .utf8)!)
//            print(self.body_length)
            self.body = self.data.prefix(Int(self.body_length))
//            print(String(data: self.body, encoding: .utf8)!)
            self.data = Data()
            self.status = .prefix
            self.recv_done = true
        }
    }
    
    func ready() {
        if let ready_callback = self.ready_callback {
            ready_callback(self)
        }
    }
    
    func close(error: Error?) {
        self.connection.stateUpdateHandler = nil
        self.connection.cancel()
        self.ready_callback = nil
        self.recv_callback = nil
        self.send_callback = nil
        if let close_callback = self.close_callback {
            self.close_callback = nil
            close_callback(self, error)
        }
    }
}
