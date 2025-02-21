# Example ingress definition. Requires Cert Manager to have already been configured.
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: &app {{ project }}
  annotations:
    cert-manager.io/issuer: letsencrypt
spec:
  # ingressClassName: nginx
  tls:
  - hosts:
    - example.com # modify this value
    secretName: "letsencrypt-{{ project }}"
  rules:
    - host: example.com # modify this value
      http:
        paths:
          - pathType: Prefix
            path: /
            backend:
              service:
                name: *app
                port:
                  name: http
