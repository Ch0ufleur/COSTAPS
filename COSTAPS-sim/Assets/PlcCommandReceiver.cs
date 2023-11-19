using System;
using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;

public class PlcCommandReceiver : MonoBehaviour
{
    [SerializeField]
    private List<TrafficControlPanel> panels = new List<TrafficControlPanel>();

    private TcpListener tcpListener;
    private Thread tcpListenerThread;
    private TcpClient connectedTcpClient;

    public string plcIp = "127.0.0.1";
    public int plcPort = 50242;

    // Start is called before the first frame update
    void Start()
    {
        tcpListenerThread = new Thread(new ThreadStart(ListenForIncommingRequests));
        tcpListenerThread.IsBackground = true;
        tcpListenerThread.Start();
    }

    private void ListenForIncommingRequests()
    {
        try
        {
            // Create listener on port 50242.          
            tcpListener = new TcpListener(IPAddress.Parse(plcIp), plcPort);
            tcpListener.Start();
            Byte[] bytes = new Byte[1024];
            while (true)
            {
                using (connectedTcpClient = tcpListener.AcceptTcpClient())
                {
                    // Get a stream object for reading                  
                    using (NetworkStream stream = connectedTcpClient.GetStream())
                    {
                        int length;
                        // Read incoming stream into byte array.                  
                        while ((length = stream.Read(bytes, 0, bytes.Length)) != 0)
                        {
                            var incomingData = new byte[length];
                            Array.Copy(bytes, 0, incomingData, 0, length);
                            // Convert byte array to string message.                        
                            string clientMessage = Encoding.ASCII.GetString(incomingData);
                            Debug.Log("client message received as: " + clientMessage);
                        }
                    }
                }
            }
        }
        catch (SocketException socketException)
        {
            Debug.Log("SocketException " + socketException.ToString());
        }
    }

    public void Register(TrafficControlPanel trafficControlPanel)
    {
        if(trafficControlPanel == null) {
            return;
        }
        panels.Add(trafficControlPanel);
    }
}
