package com.deltaswing.data.local.database

import androidx.room.Database
import androidx.room.RoomDatabase
import com.deltaswing.data.local.dao.StockDao
import com.deltaswing.data.local.entity.StockEntity

@Database(entities = [StockEntity::class], version = 1, exportSchema = false)
abstract class AppDatabase : RoomDatabase() {
    abstract fun stockDao(): StockDao
}
