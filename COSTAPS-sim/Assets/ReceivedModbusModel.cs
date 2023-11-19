using System;
using System.Collections.Generic;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

public class ReceivedModbusModel
{
    public int id;
    public LightModel[] states;
    public string timestamp;

    public ReceivedModbusModel(int id, LightModel[] states, string timestamp = "")
    {
        this.id = id;
        this.states = states;
        this.timestamp = timestamp;
    }

    public override string ToString()
    {
        return id.ToString() + " " + states[0].green + " " + states[0].yellow + " " + states[0].green + " "+timestamp;
    }

    public static ReceivedModbusModel FromJson(string json) => JsonConvert.DeserializeObject<ReceivedModbusModel>(json);

}

public struct LightModel
{
    public short green;
    public short yellow;
    public short red;
}
