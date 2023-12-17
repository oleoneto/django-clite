apiVersion: v1
kind: Service
metadata:
  name: &app {{ project }}
spec:
  ports:
    - name: http
      port: 3000
      targetPort: http
  selector:
    app: *app