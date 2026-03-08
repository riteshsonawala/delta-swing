package com.deltaswing.data.local.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import com.deltaswing.data.local.entity.StockEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface StockDao {

    @Query("SELECT * FROM stocks WHERE userId = :userId ORDER BY symbol ASC")
    fun getStocksByUser(userId: String): Flow<List<StockEntity>>

    @Query("SELECT * FROM stocks WHERE userId = :userId")
    suspend fun getStocksByUserOnce(userId: String): List<StockEntity>

    @Query("SELECT * FROM stocks WHERE id = :stockId")
    suspend fun getStock(stockId: String): StockEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertStock(stock: StockEntity)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertStocks(stocks: List<StockEntity>)

    @Update
    suspend fun updateStock(stock: StockEntity)

    @Query("DELETE FROM stocks WHERE id = :stockId")
    suspend fun deleteStock(stockId: String)

    @Query("DELETE FROM stocks WHERE userId = :userId")
    suspend fun deleteAllForUser(userId: String)
}
