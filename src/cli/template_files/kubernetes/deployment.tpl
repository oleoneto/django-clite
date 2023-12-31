apiVersion: apps/v1
kind: Deployment
metadata:
  name: &app {{ project }}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: *app
  template:
    metadata:
      name: *app
      labels:
        app: *app
    spec:
      restartPolicy: Always
      containers:
        - name: *app
          image: &image "docker.io/{{ project }}" # modify this value
          imagePullPolicy: IfNotPresent
          securityContext:
            allowPrivilegeEscalation: false
          resources:
            limits:
              memory: "128Mi"
          ports:
            - name: &port http
              containerPort: 8080
          readinessProbe:
            httpGet:
              port: *port
              path: /robots.txt
            timeoutSeconds: 120
          livenessProbe:
            exec:
              command:
                - cat
                - /app/README.md
            timeoutSeconds: 30
          envFrom:
            - secretRef:
                name: *app
            - configMapRef:
                name: *app
      initContainers:
        - name: migrations
          image: *image
          securityContext:
            allowPrivilegeEscalation: false
          command: ["manage.py"]
          args: ["migrate"]
          envFrom:
            - secretRef:
                name: *app
            - configMapRef:
                name: *app
        - name: staticfiles
          image: *image
          securityContext:
            allowPrivilegeEscalation: false
          command: ["manage.py"]
          args: ["collectstatic", "--noinput"]
          envFrom:
            - secretRef:
                name: *app
            - configMapRef:
                name: *app
