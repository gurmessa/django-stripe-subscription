# Django stripe subscription


### install prerequisites 
```
pip install -r requirements.txt
```

### run stripe webhook
```
stripe listen --forward-to localhost:8000/webhook/
```
