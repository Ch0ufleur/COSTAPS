using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TrafficControlPanel : MonoBehaviour
{
    public GameObject NorthBound;
    public GameObject SouthBound;
    public Material Allowed;
    public Material Denied;
    public Material SlowDown;
    [SerializeField]
    private PlcCommandReceiver PlcCommandReceiver;
    [SerializeField]
    private PrefabSpawner NorthSpawner;
    [SerializeField]
    private PrefabSpawner SouthSpawner;
    [SerializeField]
    private List<StopLineColliderControler> StopLineColliderControlers = new List<StopLineColliderControler>();

    public PanelState state = PanelState.DenyAll;

    void Start()
    {
        if(NorthBound == null || SouthBound == null || PlcCommandReceiver == null)
        {
            throw new ArgumentNullException();
        }
        PlcCommandReceiver.Register(this);
        ChangeInternalMaterials();
    }

    public void RegisterStopLine(StopLineColliderControler stopLineColliderControler)
    {
        StopLineColliderControlers.Add(stopLineColliderControler);
    }

    public void UpdateState(PanelState state)
    {
        this.state = state;
        ChangeInternalMaterials();
        foreach(StopLineColliderControler c in StopLineColliderControlers)
        {
            c.UpdateColliderState(state);
        }
    }

    private void ChangeInternalMaterials()
    {
        switch(state)
        {
            case PanelState.DenyAll:
                NorthBound.GetComponent<Renderer>().material = Denied;
                SouthBound.GetComponent<Renderer>().material = Denied;
                NorthSpawner.StopSpawning();
                SouthSpawner.StopSpawning();
                break;
            case PanelState.AllowAll:
                NorthBound.GetComponent<Renderer>().material = Allowed;
                SouthBound.GetComponent<Renderer>().material = Allowed;
                NorthSpawner.StartSpawning();
                SouthSpawner.StartSpawning();
                break;
            case PanelState.NorthBound:
                NorthBound.GetComponent<Renderer>().material = Allowed;
                SouthBound.GetComponent<Renderer>().material = Denied;
                NorthSpawner.StartSpawning();
                SouthSpawner.StopSpawning();
                break;
            case PanelState.SouthBound:
                NorthBound.GetComponent<Renderer>().material = Denied;
                SouthBound.GetComponent<Renderer>().material = Allowed;
                NorthSpawner.StopSpawning();
                SouthSpawner.StartSpawning();
                break;
            case PanelState.NorthBoundYellow:
                NorthBound.GetComponent<Renderer>().material = SlowDown;
                SouthBound.GetComponent<Renderer>().material = Denied;
                NorthSpawner.StartSpawning();
                SouthSpawner.StopSpawning();
                break;
            case PanelState.SouthBoundYellow:
                NorthBound.GetComponent<Renderer>().material = Denied;
                SouthBound.GetComponent<Renderer>().material = SlowDown;
                NorthSpawner.StopSpawning();
                SouthSpawner.StartSpawning();
                break;
            case PanelState.YellowParty:
                NorthBound.GetComponent<Renderer>().material = SlowDown;
                SouthBound.GetComponent<Renderer>().material = SlowDown;
                NorthSpawner.StopSpawning();
                SouthSpawner.StartSpawning();
                break;
            default:
                NorthBound.GetComponent<Renderer>().material = Denied;
                SouthBound.GetComponent<Renderer>().material = Denied;
                NorthSpawner.StopSpawning();
                SouthSpawner.StopSpawning();
                break;

        }
    }
}
