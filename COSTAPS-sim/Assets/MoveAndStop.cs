using UnityEditor;
using UnityEngine;
using UnityEngine.Animations;

public class MoveAndStop : MonoBehaviour
{
    public float initialSpeed = 10f; // The initial speed at which the object moves
    public float deceleration = 0.5f; // The rate of deceleration when an object is detected
    public float acceleration = 0.5f; // The rate of acceleration when no object is detected
    public float detectionDistance = 5f; // The distance at which the raycast can detect objects
    private float lifeTime = 0;
    private float speed; // The current speed
    private Rigidbody rb;

    void Start()
    {
        rb = GetComponent<Rigidbody>();
        speed = initialSpeed;
    }

    private void OnDestroy()
    {
        Debug.Log(lifeTime);/*
        if (EditorApplication.isPlaying && GameObject.Find("PLCCommandReceiver").GetComponent<PlcCommandReceiver>().simulationType == SimulationType.Grocery)
        {
            EditorApplication.isPlaying = false;
        }*/
    }

    void FixedUpdate()
    {
        lifeTime += Time.fixedDeltaTime;
        // Cast a ray forward from the object's position in the x direction
        Ray ray = new Ray(transform.position, transform.right);
        RaycastHit hit;

        // If the ray hits an object within detectionDistance
        if (Physics.Raycast(ray, out hit, detectionDistance))
        {
            if(hit.collider.gameObject.GetComponent<StopLineColliderControler>() != null)
            {
                if (hit.collider.gameObject.GetComponent<StopLineColliderControler>().stopLineState == StopLineState.Stop)
                {
                    // Debug.Log(hit.distance);
                    if(hit.collider.gameObject.tag == "turnPoint" && hit.distance < 6f)
                    {
                        // Debug.Log("turnPoint");
                        transform.Rotate(new Vector3(0, 1, 0), 90);
                    }
                    else
                    {
                        speed = Mathf.MoveTowards(speed, 0, deceleration * Time.fixedDeltaTime);
                    }
                }
                else if (hit.collider.gameObject.GetComponent<StopLineColliderControler>().stopLineState == StopLineState.Slow)
                {
                    if (hit.distance < detectionDistance / 2)
                    {
                        speed = Mathf.MoveTowards(speed, initialSpeed, acceleration * Time.fixedDeltaTime);
                    }
                    else
                    {
                        speed = Mathf.MoveTowards(speed, 0, deceleration * Time.fixedDeltaTime * (detectionDistance/9));
                    }
                }
                else
                {
                    speed = Mathf.MoveTowards(speed, initialSpeed, acceleration * Time.fixedDeltaTime);
                }
            }
            else
            {
                speed = Mathf.MoveTowards(speed, 0, deceleration * Time.fixedDeltaTime);
            }

        }
        else
        {
            // If no object is detected, accelerate back to the initial speed
            speed = Mathf.MoveTowards(speed, initialSpeed, acceleration * Time.fixedDeltaTime);
        }

        // Apply the velocity
        rb.velocity = transform.right * speed;
    }
}
