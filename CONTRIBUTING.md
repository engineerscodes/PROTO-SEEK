# Contributing to this repository

# Getting started
# Before you begin
  * make sure to setup smtp2go or you change it to smtp
1. Add Validation in  form.py 
2. add reverse lookup for ForeignKey using Model_set
```python
class A(models.Model):
    pass

class B(models.Model):
    b= models.ForeignKey(A, on_delete=models.CASCADE)
  
#c is an instance of A
>>> c.B_set.all()
```
