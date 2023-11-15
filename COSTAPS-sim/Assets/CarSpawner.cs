using UnityEngine;

public class PrefabSpawner : MonoBehaviour
{
    public GameObject prefab; // The prefab to spawn
    public float spawnInterval = 5f; // The interval at which the prefab will be spawned

    public void StartSpawning()
    {
        StopSpawning();
        // Call the SpawnPrefab method every spawnInterval seconds
        InvokeRepeating("SpawnPrefab", spawnInterval, spawnInterval);
    }

    void SpawnPrefab()
    {
        // Instantiate the prefab at the position of the GameObject
        Instantiate(prefab, transform.position, transform.rotation);
    }

    public void StopSpawning()
    {
        // Cancel the repeating method
        CancelInvoke("SpawnPrefab");
    }
}