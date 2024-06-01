# customer.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("app.log"),
                              logging.StreamHandler()])
logger = logging.getLogger(__name__)

app = FastAPI()

class Search(BaseModel):
    CustomerID: int

@app.post("/search/")
async def get_customer(search: Search):
    if search.CustomerID > 200000:
        logger.warning("Invalid CustomerID: %s", search.CustomerID)
        raise HTTPException(status_code=400, detail="Invalid CustomerID: Value must be less than or equal to 200000")

    try:
        logger.info("Connecting to database")
        conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            database='deepak',
            user='root',
            password='Deepak@2005'
        )

        if conn.is_connected():
            logger.info("Connected to database")
            cursor = conn.cursor()
            query = 'SELECT * FROM customer WHERE CustomerID = %s'
            logger.debug("Executing query: %s with CustomerID: %s", query, search.CustomerID)
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
            logger.info("Query successful, returning results")
            return customers
        else:
            logger.error("Failed to connect to the database")
            raise HTTPException(status_code=500, detail="Failed to connect to the database")
    except Error as e:
        logger.error("Database error: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
