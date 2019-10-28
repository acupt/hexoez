# hexoez

For hexo markdown files' properties (tags/title/categories...), batch add/del/update...

## hexoez

批量修改指定目录中md文件的属性，如tags,categories,title

```
python hexoez.py <op> <target> <argv> <file>
```

### 增加tag

给hexoez.md增加tag，可以多个

```
python hexoez.py add tags newTag1 "new tag2" tag3 source/hexoez.md
```

给指定目录(包括子目录)下所有md文件增加tag，其他命令的批量操作类似，最后的参数不是.md结尾默认为目录

```
python hexoez.py add tags newTag1 "new tag2" tag3 source/
```

### 删除tag

```
python hexoez.py del tags newTag1 "new tag2" tag3 source/hexoez.md
```

### 修改tag

```
python hexoez.py update tags old_tag new_tag source/hexoez.md
```

### 修改标题

```
python hexoez.py update title old_title new_title source/hexoez.md
```

