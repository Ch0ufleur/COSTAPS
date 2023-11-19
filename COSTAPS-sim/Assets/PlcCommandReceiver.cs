using System;
using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Reflection;
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

    public SimulationType simulationType = SimulationType.Bridge;

    // Start is called before the first frame update
    void Start()
    {
        if (panels.Count == 0)
            throw new TargetParameterCountException();
        tcpListenerThread = new Thread(new ThreadStart(ListenForIncommingRequests));
        tcpListenerThread.IsBackground = true;
        tcpListenerThread.Start();
    }

    private void ListenForIncommingRequests()
    {
        try
        {
            // Create listener on localhost port 12345. 			
            tcpListener = new TcpListener(IPAddress.Parse("127.0.0.1"), 12345);
            tcpListener.Start();
            Debug.Log("Server is listening");
            Byte[] bytes = new Byte[1024];
            while (true)
            {
                using (connectedTcpClient = tcpListener.AcceptTcpClient())
                {
                    // Get a stream object for reading 					
                    using (NetworkStream stream = connectedTcpClient.GetStream())
                    {
                        int length;
                        // Read incomming stream into byte arrary. 						
                        while ((length = stream.Read(bytes, 0, bytes.Length)) != 0)
                        {
                            var incommingData = new byte[length];
                            Array.Copy(bytes, 0, incommingData, 0, length);
                            // Convert byte array to string message. 							
                            string clientMessage = Encoding.ASCII.GetString(incommingData);
                            HandleTcpRequest(clientMessage);
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

    private void HandleTcpRequest(string clientMessage)
    {
        MainThreadDispatcher.Execute(() =>
        {
            ReceivedModbusModel model = ReceivedModbusModel.FromJson(clientMessage);
            model.id--; // le genre de chose qu'on touche pas même si on comprend pas pourquoi
            AdaptPanelStates(model);
        });
    }

    private void AdaptPanelStates(ReceivedModbusModel model)
    {
        PanelState newState = PanelState.DenyAll;
        if(model.states.Length != 2)
        {
            panels[model.id].UpdateState(newState);
            return;
        }
        if(simulationType == SimulationType.Crossway)
        {
            

        }
        if (simulationType == SimulationType.Bridge)
        {
            if (model.states[0].red == 1 && model.states[1].green == 1)
            {
                newState = PanelState.SouthBound;
            }
            else if (model.states[0].green == 1 && model.states[1].red == 1)
            {
                newState = PanelState.NorthBound;
            }
            else if (model.states[0].green == 1 && model.states[1].green == 1)
            {
                newState = PanelState.AllowAll;
            }
            else
            {
                newState = PanelState.DenyAll;
            }
        }
        panels[model.id].UpdateState(newState);
    }
}
