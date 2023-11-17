using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ButtonAction : MonoBehaviour
{
    public Button btn;

    void Start()
    {
        btn.onClick.AddListener(ChangeLightState);
    }
    public void ChangeLightState()
    {
        GameObject.FindGameObjectWithTag("controlPanel").GetComponent<TrafficControlPanel>().UpdateState(PanelState.NorthBoundYellow);
    }
}
