# Rick and Morty K8s Automation

## Workflow & Pipeline Explanation
This project uses **GitHub Actions** to automate the deployment lifecycle:

1. **Job: kubernetes-test**:
   - **Environment**: Runs on `ubuntu-latest`.
   - **Cluster**: Uses `Kind` (Kubernetes in Docker) to create a lightweight local cluster for testing.
   - **Build**: Builds the Docker image and loads it directly into the Kind node.
   - **Deploy**: Uses `Helm` to install the chart using the `v6` image tag.
   - **Test**: 
     - Verifies the Pod reaches a `Ready` state.
     - Inspects logs for the `SUCCESS` status code.
     - Confirms the `results.csv` was written to the `emptyDir` volume mount at `/app/data/`.

## Why Volumes?
I used an `emptyDir` volume to ensure the data persists even if the container finishes its execution. This allows us to use `kubectl cp` or `kubectl exec` to retrieve the data during the Pod's grace period.