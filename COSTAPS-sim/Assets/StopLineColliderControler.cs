using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class StopLineColliderControler : MonoBehaviour
{
    public TrafficControlPanel tcp;
    public StopLineState stopLineState;
    private BoxCollider stopLineCollider;

    private void Awake()
    {
        stopLineCollider = gameObject.GetComponent<BoxCollider>();
    }

    private void Start()
    {
        tcp.RegisterStopLine(this);
    }

    public void UpdateColliderState(PanelState state)
    {
        switch(state)
        {
            case PanelState.NorthBoundYellow:
            case PanelState.SouthBoundYellow:
            case PanelState.YellowParty:
                stopLineState = StopLineState.Slow;
                break;
            case PanelState.AllowAll:
                stopLineState = StopLineState.Go;
                break;
            case PanelState.DenyAll:
            default:
                stopLineState = StopLineState.Stop;
                break;
        }
    }
}

public enum StopLineState
{
    Go, Slow, Stop
}
