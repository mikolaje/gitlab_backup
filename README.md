### Usage
```
python backup.py -c template.yml
```



### Example
You can take the below template.yaml config file as example:
```yaml
private_token: abcd  # your private token provided from gitlab
destpath: /tmp/gitlab  # the path you want to place all of your gitlab repos
```

After setup the config file, just run: `python backup.py -c template.yml`
