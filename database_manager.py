import psycopg2
from psycopg2 import sql
from psycopg2.extras import Json
from typing import Dict, List, Any, Optional

class DatabaseManager:
    def __init__(self, db_config: Dict[str, str]):
        self.db_config = db_config
        self.conn = None
        self.connect()

    def connect(self):
        """Establishes a connection to the PostgreSQL database."""
        try:
            self.conn = psycopg2.connect(**self.db_config)
            self.conn.autocommit = True # Auto-commit transactions
            print("Database connection established successfully.")
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")
            self.conn = None

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

    def _execute_query(self, query: sql.Composable, params: Optional[Tuple] = None, fetch_one=False, fetch_all=False):
        """Helper to execute SQL queries."""
        if not self.conn:
            self.connect() # Attempt to reconnect
            if not self.conn:
                raise ConnectionError("No database connection available.")

        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                if fetch_one:
                    return cur.fetchone()
                if fetch_all:
                    return cur.fetchall()
                return None
        except psycopg2.Error as e:
            print(f"Database error during query execution: {e}")
            self.conn.rollback() # Rollback on error
            raise # Re-raise the exception

    def setup_database(self, schema_sql_path: str):
        """Executes the database schema creation script."""
        with open(schema_sql_path, 'r') as f:
            schema_script = f.read()
        self._execute_query(sql.SQL(schema_script))
        print("Database schema setup complete.")

    def insert_sample_data(self, sample_data_sql_path: str):
        """Inserts sample data into the database."""
        with open(sample_data_sql_path, 'r') as f:
            sample_data_script = f.read()
        self._execute_query(sql.SQL(sample_data_script))
        print("Sample data inserted.")

    # --- User Profile Management ---
    def insert_user_profile(self, user_profile: Dict[str, Any]):
        query = sql.SQL("""
            INSERT INTO user_profiles (user_id, demographics, learning_preferences, behavioral_patterns, engagement_metrics)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE
            SET demographics = EXCLUDED.demographics,
                learning_preferences = EXCLUDED.learning_preferences,
                behavioral_patterns = EXCLUDED.behavioral_patterns,
                engagement_metrics = EXCLUDED.engagement_metrics;
        """)
        self._execute_query(query, (
            user_profile['user_id'],
            Json(user_profile.get('demographics', {})),
            Json(user_profile.get('learning_preferences', {})),
            Json(user_profile.get('behavioral_patterns', {})),
            Json(user_profile.get('engagement_metrics', {}))
        ))

    def fetch_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        query = sql.SQL("SELECT user_id, demographics, learning_preferences, behavioral_patterns, engagement_metrics FROM user_profiles WHERE user_id = %s;")
        row = self._execute_query(query, (user_id,), fetch_one=True)
        if row:
            return {
                "user_id": row[0],
                "demographics": row[1],
                "learning_preferences": row[2],
                "behavioral_patterns": row[3],
                "engagement_metrics": row[4],
            }
        return None

    def fetch_all_user_profiles(self) -> Dict[str, Dict[str, Any]]:
        query = sql.SQL("SELECT user_id, demographics, learning_preferences, behavioral_patterns, engagement_metrics FROM user_profiles;")
        rows = self._execute_query(query, fetch_all=True)
        profiles = {}
        for row in rows:
            profiles[row[0]] = {
                "user_id": row[0],
                "demographics": row[1],
                "learning_preferences": row[2],
                "behavioral_patterns": row[3],
                "engagement_metrics": row[4],
            }
        return profiles

    def get_all_user_ids(self) -> List[str]:
        query = sql.SQL("SELECT user_id FROM user_profiles;")
        rows = self._execute_query(query, fetch_all=True)
        return [row[0] for row in rows]

    def get_total_users(self) -> int:
        query = sql.SQL("SELECT COUNT(*) FROM user_profiles;")
        return self._execute_query(query, fetch_one=True)[0]

    # --- Learning Session Management ---
    def insert_learning_session(self, session: Dict[str, Any]):
        query = sql.SQL("""
            INSERT INTO learning_sessions (session_id, user_id, content_accessed, time_spent, interactions, performance_metrics, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """)
        self._execute_query(query, (
            session['session_id'],
            session['user_id'],
            Json(session.get('content_accessed', [])),
            session.get('time_spent'), # This should be a string like 'PT1H30M' or timedelta in Python
            Json(session.get('interactions', {})),
            Json(session.get('performance_metrics', {})),
            session.get('timestamp') # Datetime object
        ))

    def fetch_user_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        query = sql.SQL("SELECT session_id, user_id, content_accessed, time_spent, interactions, performance_metrics, timestamp FROM learning_sessions WHERE user_id = %s ORDER BY timestamp ASC;")
        rows = self._execute_query(query, (user_id,), fetch_all=True)
        sessions = []
        for row in rows:
            sessions.append({
                "session_id": row[0],
                "user_id": row[1],
                "content_accessed": row[2],
                "time_spent": row[3],
                "interactions": row[4],
                "performance_metrics": row[5],
                "timestamp": row[6]
            })
        return sessions

    def fetch_all_learning_sessions(self) -> List[Dict[str, Any]]:
        query = sql.SQL("SELECT session_id, user_id, content_accessed, time_spent, interactions, performance_metrics, timestamp FROM learning_sessions;")
        rows = self._execute_query(query, fetch_all=True)
        sessions = []
        for row in rows:
            sessions.append({
                "session_id": row[0],
                "user_id": row[1],
                "content_accessed": row[2],
                "time_spent": row[3],
                "interactions": row[4],
                "performance_metrics": row[5],
                "timestamp": row[6]
            })
        return sessions

    # --- Analytics Data Storage (Engineered Features, Predictions, Recommendations, Insights) ---
    def update_user_features(self, user_id: str, features: Dict[str, Any]):
        query = sql.SQL("""
            INSERT INTO user_analytics_data (user_id, engineered_features)
            VALUES (%s, %s)
            ON CONFLICT (user_id) DO UPDATE SET engineered_features = EXCLUDED.engineered_features;
        """)
        self._execute_query(query, (user_id, Json(features)))

    def fetch_user_features(self, user_id: str) -> Optional[Dict[str, Any]]:
        query = sql.SQL("SELECT engineered_features FROM user_analytics_data WHERE user_id = %s;")
        row = self._execute_query(query, (user_id,), fetch_one=True)
        return row[0] if row else None

    def fetch_all_user_features(self) -> Dict[str, Dict[str, Any]]:
        query = sql.SQL("SELECT user_id, engineered_features FROM user_analytics_data;")
        rows = self._execute_query(query, fetch_all=True)
        features = {}
        for row in rows:
            features[row[0]] = row[1]
        return features

    def update_user_cluster(self, user_id: str, cluster_label: int):
        query = sql.SQL("""
            INSERT INTO user_analytics_data (user_id, cluster_label)
            VALUES (%s, %s)
            ON CONFLICT (user_id) DO UPDATE SET cluster_label = EXCLUDED.cluster_label;
        """)
        self._execute_query(query, (user_id, cluster_label))

    def fetch_user_cluster(self, user_id: str) -> Optional[int]:
        query = sql.SQL("SELECT cluster_label FROM user_analytics_data WHERE user_id = %s;")
        row = self._execute_query(query, (user_id,), fetch_one=True)
        return row[0] if row else None

    def fetch_features_by_cluster(self, cluster_label: int) -> Dict[str, Dict[str, Any]]:
        query = sql.SQL("SELECT user_id, engineered_features FROM user_analytics_data WHERE cluster_label = %s;")
        rows = self._execute_query(query, (cluster_label,), fetch_all=True)
        features = {}
        for row in rows:
            features[row[0]] = row[1]
        return features

    def update_user_predictions(self, user_id: str, prediction_type: str, prediction_data: Any):
        # This approach updates a JSONB field.
        # For 'performance', 'optimal_study_time', etc.
        query = sql.SQL(f"""
            UPDATE user_analytics_data
            SET predictions = jsonb_set(coalesce(predictions, '{{}}'::jsonb), %s, %s, true)
            WHERE user_id = %s;
        """)
        self._execute_query(query, ([prediction_type], Json(prediction_data), user_id))

    def fetch_user_predictions(self, user_id: str) -> Optional[Dict[str, Any]]:
        query = sql.SQL("SELECT predictions FROM user_analytics_data WHERE user_id = %s;")
        row = self._execute_query(query, (user_id,), fetch_one=True)
        return row[0] if row else None

    def update_user_recommendations(self, user_id: str, recommendations: List[Dict[str, Any]]):
        query = sql.SQL("""
            UPDATE user_analytics_data
            SET recommendations = %s
            WHERE user_id = %s;
        """)
        self._execute_query(query, (Json(recommendations), user_id))

    def fetch_user_recommendations(self, user_id: str) -> Optional[List[Dict[str, Any]]]:
        query = sql.SQL("SELECT recommendations FROM user_analytics_data WHERE user_id = %s;")
        row = self._execute_query(query, (user_id,), fetch_one=True)
        return row[0] if row else None

    def update_user_insights(self, user_id: str, insights: Dict[str, str]):
        query = sql.SQL("""
            UPDATE user_analytics_data
            SET insights = %s
            WHERE user_id = %s;
        """)
        self._execute_query(query, (Json(insights), user_id))

    def fetch_user_insights(self, user_id: str) -> Optional[Dict[str, str]]:
        query = sql.SQL("SELECT insights FROM user_analytics_data WHERE user_id = %s;")
        row = self._execute_query(query, (user_id,), fetch_one=True)
        return row[0] if row else None

    def fetch_all_learning_outcomes(self) -> Dict[str, float]:
        """Fetches the average quiz score for each user to be used as ML target."""
        query = sql.SQL("""
            SELECT
                ls.user_id,
                AVG((ls.performance_metrics->>'score')::numeric) as avg_score
            FROM
                learning_sessions ls
            WHERE
                ls.performance_metrics->>'score' IS NOT NULL
            GROUP BY
                ls.user_id;
        """)
        rows = self._execute_query(query, fetch_all=True)
        return {row[0]: float(row[1]) for row in rows}

    def fetch_user_completed_content(self, user_id: str) -> List[str]:
        query = sql.SQL("""
            SELECT DISTINCT jsonb_array_elements_text(content_accessed)
            FROM learning_sessions
            WHERE user_id = %s;
        """)
        rows = self._execute_query(query, (user_id,), fetch_all=True)
        return [row[0] for row in rows if row and row[0]] # Filter out None or empty strings

    def fetch_top_content_by_cluster(self, cluster_label: int, limit: int = 5) -> Dict[str, int]:
        """Fetches most frequently accessed content by users in a specific cluster."""
        query = sql.SQL("""
            SELECT
                jsonb_array_elements_text(ls.content_accessed) as content_id,
                COUNT(*) as access_count
            FROM
                learning_sessions ls
            JOIN
                user_analytics_data uad ON ls.user_id = uad.user_id
            WHERE
                uad.cluster_label = %s
            GROUP BY
                content_id
            ORDER BY
                access_count DESC
            LIMIT %s;
        """)
        rows = self._execute_query(query, (cluster_label, limit), fetch_all=True)
        return {row[0]: row[1] for row in rows}
    