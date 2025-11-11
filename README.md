# ⚽ Football Tactical Intelligence Platform

A Streamlit application for uploading, processing, and analyzing SkillCorner football match data.

## 🎯 Features

- **Data Upload Interface**: Upload SkillCorner dataset (metadata, tracking, events, phases)
- **Data Pre-processing**: Automatically create enriched tracking data by merging tracking data with player metadata
- **Knowledge Bank Generation**: Comprehensive field documentation for all datasets
- **Interactive Data Viewer**: Filter and explore enriched tracking data
- **Export Capabilities**: Download processed data in CSV format

## 📋 Requirements

### Dataset Files

The application requires four SkillCorner dataset files:

1. **Metadata (JSON)**: Match information, team data, player details, pitch dimensions
2. **Tracking Data (JSONL)**: Frame-by-frame player and ball positions (10 FPS)
3. **Events (CSV)**: Match events including passes, shots, tackles, and advanced metrics
4. **Phases (CSV)**: Team possession and phase of play information

### System Requirements

- Python 3.8+
- See `requirements.txt` for package dependencies

## 🚀 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Fchat
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## 📁 Project Structure

```
Fchat/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── claude.md                       # Detailed specification
│
├── config/                         # Configuration files
├── data/
│   ├── uploads/                   # User uploaded files
│   ├── processed/                 # Processed data (parquet files)
│   └── cache/                     # Cached computations & knowledge bank
│
├── src/
│   ├── data_processing/
│   │   ├── preprocessing.py       # Data preprocessing logic
│   │   └── knowledge_bank.py      # Knowledge bank generator
│   ├── analytics/                 # Analytics modules (future)
│   ├── video/                     # Video processing (future)
│   ├── chat/                      # Chat interface (future)
│   ├── report/                    # Report generation (future)
│   └── ui/                        # UI components (future)
│
├── clips/                         # Generated video clips (future)
└── outputs/                       # Exported reports (future)
```

## 📖 Usage

### 1. Upload Data

1. Navigate to the "Upload Data" page
2. Upload all four required files:
   - Match Metadata (JSON)
   - Tracking Data (JSONL)
   - Events Data (CSV)
   - Phases of Play (CSV)
3. Enter a unique Match ID
4. Click "Process Data" to start processing

### 2. View Enriched Data

After processing, navigate to "View Enriched Data" to:
- View dataset summary statistics
- See match information
- Filter data by period and team
- Download processed data as CSV

### 3. Explore Knowledge Bank

Navigate to "Knowledge Bank" to:
- Browse field documentation for all datasets
- Search for specific fields
- View critical fields and data types
- Download the complete knowledge bank as JSON

## 🔍 Data Processing

### Enriched Tracking Data

The application creates enriched tracking data by:

1. **Loading Tracking Data**: Reads frame-by-frame position data
2. **Processing Metadata**: Extracts player information and team details
3. **Merging Data**: Combines tracking positions with player context
4. **Adding Features**:
   - Player position and role
   - Team affiliation (home/away)
   - Direction of play per half
   - Playing time statistics
   - Goalkeeper flags

### Knowledge Bank

The knowledge bank documents:

- **Field Names**: All available fields in each dataset
- **Data Types**: Type information for each field
- **Critical Fields**: Key fields identified per dataset
- **Field Categories**: Organized grouping of related fields
- **Sample Values**: Example values for understanding data structure
- **Descriptions**: Context and usage information

## 🎨 UI/UX

The application follows a clean, professional design with:

- **Color Scheme**:
  - Primary: #00A85D (Vivid Green)
  - Secondary: #1D73E8 (Bold Blue)
  - Accent: #00D8B0 (Teal)
  - Success: #4CAF50
  - Warning: #FFB300
  - Danger: #D32F2F

- **Layout**: Wide layout with sidebar navigation
- **Components**:
  - File uploaders with helpful tooltips
  - Progress bars for processing feedback
  - Interactive data tables with filters
  - Expandable sections for detailed information

## 📊 Data Schema

### Enriched Tracking Data Fields

The enriched tracking data includes:

- **Temporal**: frame, timestamp, period
- **Spatial**: x, y (player position), ball_x, ball_y, ball_z
- **Player Info**: player_id, short_name, number, team_name
- **Tactical**: player_role, position_group, direction_player (per half)
- **Context**: match_name, home_away_player, is_gk
- **Possession**: possession_player_id, possession_group

## 🔮 Future Enhancements

Based on the full specification in `claude.md`, future phases will include:

- **Analytics Dashboard**: 14-section match analysis report
- **Video Generation**: Automatic clip generation for key moments
- **Chat Interface**: AI-powered match analysis with natural language queries
- **Advanced Metrics**: xG, pressing metrics, formation analysis
- **Report Export**: PDF, HTML, and PowerPoint exports

## 🐛 Troubleshooting

### Common Issues

1. **File Upload Errors**: Ensure files are in the correct format (JSON, JSONL, CSV)
2. **Memory Issues**: For large tracking files, consider processing in chunks
3. **Missing Fields**: Verify that your data schema matches SkillCorner format

## 📝 License

See LICENSE file for details.

## 👥 Contributing

Contributions are welcome! Please read the contributing guidelines before submitting pull requests.

## 📧 Contact

For questions or support, please open an issue in the repository.

---

Built with ❤️ using Streamlit and Python
