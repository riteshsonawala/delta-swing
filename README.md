# Delta Swing

A native Android stock portfolio tracker that monitors price dips and sends morning notifications when stocks drop below a user-defined threshold.

## Features

- **Google Sign-In** via Firebase Authentication
- **Portfolio Management** — add, edit, and delete stocks with custom base prices and delta swing thresholds
- **Real-Time Prices** via Alpha Vantage API
- **Morning Notifications** — daily 8:00 AM check using WorkManager; alerts when stocks drop below your threshold
- **Price History** — 30-day sparkline chart on the stock detail screen
- **Cloud Sync** — local Room database synced with Firebase Firestore per user
- **Dark Mode** — full Material Design 3 with dynamic color support

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Kotlin |
| UI | Jetpack Compose + Material 3 |
| Auth | Firebase Authentication (Google Sign-In) |
| Local DB | Room |
| Cloud DB | Firebase Firestore |
| Networking | Retrofit + OkHttp + Moshi |
| Stock Data | Alpha Vantage API |
| Background | WorkManager |
| DI | Hilt |
| Build | Gradle with version catalogs |

## Setup

### 1. Alpha Vantage API Key

1. Go to [alphavantage.co](https://www.alphavantage.co/support/#api-key) and get a free API key
2. Add it to your `local.properties` file:

```properties
ALPHA_VANTAGE_API_KEY=your_api_key_here
```

### 2. Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/) and create a new project
2. Add an Android app with package name `com.deltaswing`
3. Download `google-services.json` and place it in the `app/` directory
4. Enable **Authentication** → **Google Sign-In** in the Firebase Console
5. Enable **Cloud Firestore** in the Firebase Console
6. Copy the **Web client ID** from Firebase Authentication settings and update `app/src/main/res/values/strings.xml`:

```xml
<string name="default_web_client_id">YOUR_ACTUAL_WEB_CLIENT_ID</string>
```

### 3. Run the App

```bash
# Clone the repo
git clone <repo-url>
cd delta-swing

# Open in Android Studio and sync Gradle
# Or build from command line:
./gradlew assembleDebug
```

## Project Structure

```
app/src/main/java/com/deltaswing/
├── DeltaSwingApp.kt                 # Application class (Hilt, WorkManager, notifications)
├── di/
│   └── AppModule.kt                 # Hilt dependency injection module
├── domain/
│   ├── model/
│   │   ├── Stock.kt                 # Stock domain model
│   │   └── PricePoint.kt            # Price history data point
│   └── repository/
│       ├── AuthRepository.kt        # Auth interface
│       └── StockRepository.kt       # Stock data interface
├── data/
│   ├── local/
│   │   ├── entity/StockEntity.kt    # Room entity
│   │   ├── dao/StockDao.kt          # Room DAO
│   │   └── database/AppDatabase.kt  # Room database
│   ├── remote/
│   │   ├── api/AlphaVantageApi.kt   # Retrofit API interface
│   │   └── dto/                     # API response DTOs
│   ├── repository/
│   │   ├── AuthRepositoryImpl.kt    # Firebase Auth implementation
│   │   └── StockRepositoryImpl.kt   # Stock repository implementation
│   └── worker/
│       └── StockPriceCheckWorker.kt # WorkManager morning job
└── presentation/
    ├── MainActivity.kt              # Entry point, schedules WorkManager
    ├── theme/Theme.kt               # Material 3 theme
    ├── navigation/                  # Nav graph and routes
    ├── auth/                        # Sign-in screen
    ├── portfolio/                   # Portfolio list screen
    ├── addstock/                    # Add/Edit stock screen
    └── stockdetail/                 # Stock detail with sparkline
```

## How It Works

1. **Sign in** with your Google account
2. **Add stocks** to your portfolio with a symbol, base price, and delta swing percentage
3. **View current prices** — tap refresh to fetch latest from Alpha Vantage
4. **Get notified** — every morning at 8:00 AM, the app checks if any stock has dropped below your threshold and sends a notification
5. **Tap a stock** to see its 30-day price history sparkline and detailed info
6. **Swipe to delete** stocks from your portfolio
