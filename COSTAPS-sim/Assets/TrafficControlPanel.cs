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
    private PrefabSpawner NorthSpawner;
    [SerializeField]
    private PrefabSpawner SouthSpawner;
    [SerializeField]
    private List<StopLineColliderControler> StopLineColliderControlers = new List<StopLineColliderControler>();

    private Renderer NorthRenderer;
    private Renderer SouthRenderer;

    public PanelState state = PanelState.DenyAll;

    void Start()
    {
        if(NorthBound == null || SouthBound == null)
        {
            throw new ArgumentNullException();
        }
        NorthRenderer = NorthBound.GetComponent<Renderer>();
        SouthRenderer = SouthBound.GetComponent<Renderer>();
        ChangeInternalMaterials();
    }

    public void RegisterStopLine(StopLineColliderControler stopLineColliderControler)
    {
        StopLineColliderControlers.Add(stopLineColliderControler);
    }

    public void UpdateState(PanelState state)
    {
        if(this.state == state)
        {
            return;
        }
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
                NorthRenderer.material = Denied;
                SouthRenderer.material = Denied;
                NorthSpawner.StopSpawning();
                SouthSpawner.StopSpawning();
                break;
            case PanelState.AllowAll:
                NorthRenderer.material = Allowed;
                SouthRenderer.material = Allowed;
                NorthSpawner.StartSpawning();
                SouthSpawner.StartSpawning();
                break;
            case PanelState.NorthBound:
                NorthRenderer.material = Allowed;
                SouthRenderer.material = Denied;
                NorthSpawner.StartSpawning();
                SouthSpawner.StopSpawning();
                break;
            case PanelState.SouthBound:
                NorthRenderer.material = Denied;
                SouthRenderer.material = Allowed;
                NorthSpawner.StopSpawning();
                SouthSpawner.StartSpawning();
                break;
            case PanelState.NorthBoundYellow:
                NorthRenderer.material = SlowDown;
                SouthRenderer.material = Denied;
                NorthSpawner.StartSpawning();
                SouthSpawner.StopSpawning();
                break;
            case PanelState.SouthBoundYellow:
                NorthRenderer.material = Denied;
                SouthRenderer.material = SlowDown;
                NorthSpawner.StopSpawning();
                SouthSpawner.StartSpawning();
                break;
            case PanelState.YellowParty:
                NorthRenderer.material = SlowDown;
                SouthRenderer.material = SlowDown;
                NorthSpawner.StopSpawning();
                SouthSpawner.StartSpawning();
                break;
            default:
                NorthRenderer.material = Denied;
                SouthRenderer.material = Denied;
                NorthSpawner.StopSpawning();
                SouthSpawner.StopSpawning();
                break;

        }
    }
}
