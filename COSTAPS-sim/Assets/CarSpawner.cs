using UnityEngine;
using System;

public class PrefabSpawner : MonoBehaviour
{
    public GameObject[] prefabs; // The prefab to spawn
    public float spawnInterval = 5f; // The interval at which the prefab will be spawned
    public int limit = 30;
    private int carCount = 0;

    public void StartSpawning()
    {
        StopSpawning();
        // Call the SpawnPrefab method every spawnInterval seconds
        InvokeRepeating("SpawnPrefab", spawnInterval, spawnInterval);

    }

    void SpawnPrefab()
    {
        System.Random rand = new System.Random();
        // Cast a ray forward from the object's position in the x direction
        Ray ray = new Ray(transform.position, transform.right);
        RaycastHit hit;

        // If the ray hits an object within detectionDistance
        if (Physics.Raycast(ray, out hit, 10))
        {
            return;
        }

        // Instantiate the prefab at the position of the GameObject
        if(carCount<limit) Instantiate(prefabs[rand.Next(0,prefabs.Length)], transform.position, transform.rotation);
        carCount++;
    }

    public void StopSpawning()
    {
        // Cancel the repeating method
        CancelInvoke("SpawnPrefab");
    }
}