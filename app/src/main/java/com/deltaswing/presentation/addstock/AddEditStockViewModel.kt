package com.deltaswing.presentation.addstock

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.deltaswing.domain.model.Stock
import com.deltaswing.domain.repository.AuthRepository
import com.deltaswing.domain.repository.StockRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

data class AddEditStockUiState(
    val symbol: String = "",
    val basePrice: String = "",
    val deltaPercentage: String = "5.0",
    val isLoading: Boolean = false,
    val isSaved: Boolean = false,
    val isEditing: Boolean = false,
    val error: String? = null
)

@HiltViewModel
class AddEditStockViewModel @Inject constructor(
    private val stockRepository: StockRepository,
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(AddEditStockUiState())
    val uiState: StateFlow<AddEditStockUiState> = _uiState.asStateFlow()

    private var existingStockId: String? = null

    fun loadStock(stockId: String?) {
        if (stockId == null) return
        existingStockId = stockId
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true)
            val stock = stockRepository.getStock(stockId)
            if (stock != null) {
                _uiState.value = _uiState.value.copy(
                    symbol = stock.symbol,
                    basePrice = stock.basePrice.toString(),
                    deltaPercentage = stock.deltaPercentage.toString(),
                    isLoading = false,
                    isEditing = true
                )
            } else {
                _uiState.value = _uiState.value.copy(isLoading = false, error = "Stock not found")
            }
        }
    }

    fun updateSymbol(symbol: String) {
        _uiState.value = _uiState.value.copy(symbol = symbol.uppercase(), error = null)
    }

    fun updateBasePrice(price: String) {
        _uiState.value = _uiState.value.copy(basePrice = price, error = null)
    }

    fun updateDeltaPercentage(delta: String) {
        _uiState.value = _uiState.value.copy(deltaPercentage = delta, error = null)
    }

    fun saveStock() {
        val state = _uiState.value
        val symbol = state.symbol.trim()
        val basePrice = state.basePrice.toDoubleOrNull()
        val delta = state.deltaPercentage.toDoubleOrNull()
        val userId = authRepository.currentUser?.uid

        if (symbol.isEmpty()) {
            _uiState.value = _uiState.value.copy(error = "Enter a stock symbol")
            return
        }
        if (basePrice == null || basePrice <= 0) {
            _uiState.value = _uiState.value.copy(error = "Enter a valid base price")
            return
        }
        if (delta == null || delta <= 0 || delta > 100) {
            _uiState.value = _uiState.value.copy(error = "Enter a valid delta percentage (1-100)")
            return
        }
        if (userId == null) {
            _uiState.value = _uiState.value.copy(error = "Not signed in")
            return
        }

        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true)
            try {
                val stock = Stock(
                    id = existingStockId ?: "",
                    userId = userId,
                    symbol = symbol,
                    basePrice = basePrice,
                    deltaPercentage = delta
                )
                if (existingStockId != null) {
                    stockRepository.updateStock(stock)
                } else {
                    stockRepository.addStock(stock)
                }
                _uiState.value = _uiState.value.copy(isLoading = false, isSaved = true)
            } catch (e: Exception) {
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    error = e.message ?: "Failed to save"
                )
            }
        }
    }
}
