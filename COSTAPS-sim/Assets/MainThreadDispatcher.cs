using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class MainThreadDispatcher : MonoBehaviour
{
    private static readonly Queue<Action> ExecuteOnMainThread = new Queue<Action>();

    public void Update()
    {
        while (ExecuteOnMainThread.Count > 0)
        {
            ExecuteOnMainThread.Dequeue().Invoke();
        }
    }

    public static void Execute(Action action)
    {
        ExecuteOnMainThread.Enqueue(action);
    }
}
