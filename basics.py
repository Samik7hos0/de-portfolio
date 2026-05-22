import pandas as pd

data = {
    'order_id': [1,2,3,4,5,6,7,8],
    'customer': ['Raj','Priya','Raj','Amit','Priya','Raj','Amit','Priya'],
    'amount': [500,1200,300,800,450,900,1100,600],
    'status': ['delivered','delivered','cancelled','delivered','cancelled','delivered','delivered','cancelled']
}

df = pd.DataFrame(data)

print("\n=== Only delivered orders ===")
print(df[df['status'] == 'delivered'])