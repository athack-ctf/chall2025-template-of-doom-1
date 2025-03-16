# Running This Challenge

Build
```
docker build -t athack-ctf/chall2025-template-of-doom-1:latest .
```

Run
```
docker run -d --name template-of-doom-1 \
  --hostname template-of-doom-1 \
  -p 52047:5000 \
  athack-ctf/chall2025-template-of-doom-1:latest
```