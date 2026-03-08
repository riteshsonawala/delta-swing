package com.deltaswing.presentation.stockdetail

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.deltaswing.domain.model.PricePoint
import com.deltaswing.domain.model.Stock
import com.deltaswing.domain.repository.StockRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

data class StockDetailUiState(
    val stock: Stock? = null,
    val priceHistory: List<PricePoint> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null
)

@HiltViewModel
class StockDetailViewModel @Inject constructor(
    private val stockRepository: StockRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(StockDetailUiState())
    val uiState: StateFlow<StockDetailUiState> = _uiState.asStateFlow()

    fun loadStock(stockId: String) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true)
            try {
                val stock = stockRepository.getStock(stockId)
                if (stock != null) {
                    _uiState.value = _uiState.value.copy(stock = stock, isLoading = false)
                    // Fetch current price
                    val price = stockRepository.fetchCurrentPrice(stock.symbol)
                    if (price != null) {
                        _uiState.value = _uiState.value.copy(
                            stock = stock.copy(currentPrice = price)
                        )
                    }
                    // Fetch price history
                    val history = stockRepository.fetchPriceHistory(stock.symbol)
                    _uiState.value = _uiState.value.copy(priceHistory = history)
                } else {
                    _uiState.value = _uiState.value.copy(
                        isLoading = false,
                        error = "Stock not found"
                    )
                }
            } catch (e: Exception) {
                _uiState.value = _uiState.value.copy(
                    isLoading = false,
                    error = e.message
                )
            }
        }
    }
}
