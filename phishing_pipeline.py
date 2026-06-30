import pandas as pd
import sqlite3

# EXTRACT
columns = [
    "having_IP_Address", "URL_Length", "Shortining_Service",
    "having_At_Symbol", "double_slash_redirecting", "Prefix_Suffix",
    "having_Sub_Domain", "SSLfinal_State", "Domain_registeration_length",
    "Favicon", "port", "HTTPS_token", "Request_URL", "URL_of_Anchor",
    "Links_in_tags", "SFH", "Submitting_to_email", "Abnormal_URL",
    "Redirect", "on_mouseover", "RightClick", "popUpWidnow", "Iframe",
    "age_of_domain", "DNSRecord", "web_traffic", "Page_Rank",
    "Google_Index", "Links_pointing_to_page", "Statistical_report", "Result"
]

df = pd.read_csv('dataset.csv', names=columns)

# TRANSFORM
df['label'] = df['Result'].apply(lambda x: 'phishing' if x == -1 else 'legitimate')

# LOAD
conn = sqlite3.connect('phishing_analysis.db')
df.to_sql('url_features', conn, if_exists='replace', index=False)
print(f"Loaded {len(df)} records into SQLite")
q1 = pd.read_sql("SELECT label, COUNT(*) as total FROM url_features GROUP BY label", conn)
print("\n--- URL Distribution ---")
print(q1)

q2 = pd.read_sql("""
    SELECT label,
           ROUND(AVG(URL_Length), 2) as avg_url_length,
           ROUND(AVG(SSLfinal_State), 2) as avg_ssl_score,
           ROUND(AVG(age_of_domain), 2) as avg_domain_age
    FROM url_features GROUP BY label
""", conn)
print("\n--- Risk Signals by Class ---")
print(q2)

q3 = pd.read_sql("""
    SELECT COUNT(*) as high_risk_count FROM url_features
    WHERE having_IP_Address = 1 AND URL_Length = 1
    AND SSLfinal_State = -1 AND label = 'phishing'
""", conn)
print("\n--- High Risk Phishing URLs ---")
print(q3)

conn.close()
print("\nPipeline complete.")