package com.deltaswing.presentation.portfolio

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.deltaswing.domain.model.Stock
import com.deltaswing.domain.repository.AuthRepository
import com.deltaswing.domain.repository.StockRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.launch
import javax.inject.Inject

data class PortfolioUiState(
    val stocks: List<Stock> = emptyList(),
    val isLoading: Boolean = false,
    val isRefreshing: Boolean = false,
    val error: String? = null,
    val userName: String = ""
)

@HiltViewModel
class PortfolioViewModel @Inject constructor(
    private val stockRepository: StockRepository,
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(PortfolioUiState())
    val uiState: StateFlow<PortfolioUiState> = _uiState.asStateFlow()

    init {
        loadPortfolio()
    }

    private fun loadPortfolio() {
        val user = authRepository.currentUser ?: return
        _uiState.value = _uiState.value.copy(
            isLoading = true,
            userName = user.displayName ?: "User"
        )

        viewModelScope.launch {
            stockRepository.getStocks(user.uid)
                .catch { e ->
                    _uiState.value = _uiState.value.copy(
                        isLoading = false,
                        error = e.message
                    )
                }
                .collect { stocks ->
                    _uiState.value = _uiState.value.copy(
                        stocks = stocks,
                        isLoading = false
                    )
                }
        }
    }

    fun refreshPrices() {
        val user = authRepository.currentUser ?: return
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isRefreshing = true)
            try {
                stockRepository.refreshPrices(user.uid)
            } catch (_: Exception) { }
            _uiState.value = _uiState.value.copy(isRefreshing = false)
        }
    }

    fun deleteStock(stockId: String) {
        viewModelScope.launch {
            stockRepository.deleteStock(stockId)
        }
    }

    fun signOut() {
        viewModelScope.launch {
            authRepository.signOut()
        }
    }
}
