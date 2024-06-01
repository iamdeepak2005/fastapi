from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error

app = FastAPI()

class Search(BaseModel):
    CustomerID: int

@app.post("/search/")
async def get_customer(search: Search):
    if search.CustomerID > 200000:
        raise HTTPException(status_code=400, detail="Invalid CustomerID: Value must be less than or equal to 200000")

    try:
        conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            database='deepak',
            user='root',
            password='Deepak@2005'
        )

        if conn.is_connected():
            cursor = conn.cursor()
            query = 'SELECT * FROM customer WHERE CustomerID = %s'
            cursor.execute(query, (search.CustomerID,))
            rows = cursor.fetchall()
            customers = []
            for row in rows:
                customer = {
                    "CustomerID": row[0],
                    "CustomerName": row[1],
                    "Address": row[2],
                }
                customers.append(customer)
            cursor.close()
            conn.close()
            return customers
        else:
            raise HTTPException(status_code=500, detail="Failed to connect to the database")
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
