from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import mysql.connector
from mysql.connector import Error
import logging 
class Pledge(BaseModel):
    CustomerID: int
    CustomerName: str
    Address:str
    

def insert(pledge:Pledge):
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
            query = 'INSERT INTO customer (CustomerID, CustomerName, Address) VALUES (%s, %s, %s)'
            data = (pledge.CustomerID, pledge.CustomerName, pledge.Address)
            cursor.execute(query, data)
            conn.commit()
            cursor.close()
            conn.close()
            return {"message": "Pledge inserted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to connect to the database")

    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))
