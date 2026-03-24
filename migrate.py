import psycopg2
from urllib.parse import quote_plus

password = quote_plus("supabase@2003/2005")
# db host is usually db.PROJECT_REF.supabase.co
# if connecting via IPv4, it might require pooler... let's try db.
conn_str = f"postgresql://postgres:{password}@db.jxbtoboivebrzmilkhqp.supabase.co:6543/postgres"

print("Connecting to:", conn_str.replace(password, "HIDDEN"))

sql = """
DROP TABLE IF EXISTS reports CASCADE;
DROP TABLE IF EXISTS notifications CASCADE;
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS supports CASCADE;
DROP TABLE IF EXISTS comments CASCADE;
DROP TABLE IF EXISTS votes CASCADE;
DROP TABLE IF EXISTS idea_progress CASCADE;
DROP TABLE IF EXISTS ideas CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255),
    avatar_url TEXT,
    bio TEXT,
    college VARCHAR(255),
    department VARCHAR(255),
    year VARCHAR(50),
    city VARCHAR(100),
    domain_interests TEXT[],
    role VARCHAR(50) DEFAULT 'user',
    trust_score INT DEFAULT 100,
    followers_count INT DEFAULT 0,
    is_banned BOOLEAN DEFAULT FALSE,
    language VARCHAR(10) DEFAULT 'en',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Ideas table
CREATE TABLE IF NOT EXISTS ideas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    domain VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'Concept',
    tags TEXT[],
    required_skills TEXT[],
    upvotes_count INT DEFAULT 0,
    downvotes_count INT DEFAULT 0,
    views_count INT DEFAULT 0,
    city VARCHAR(100),
    college VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Idea Progress
CREATE TABLE IF NOT EXISTS idea_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    idea_id UUID REFERENCES ideas(id) ON DELETE CASCADE,
    update_text TEXT NOT NULL,
    stage VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Votes
CREATE TABLE IF NOT EXISTS votes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    idea_id UUID REFERENCES ideas(id) ON DELETE CASCADE,
    value INT NOT NULL, -- 1 or -1
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, idea_id)
);

-- Comments
CREATE TABLE IF NOT EXISTS comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    idea_id UUID REFERENCES ideas(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    is_anonymous BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Support Pledges
CREATE TABLE IF NOT EXISTS supports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    idea_id UUID REFERENCES ideas(id) ON DELETE CASCADE,
    supporter_id UUID REFERENCES users(id) ON DELETE CASCADE,
    pledge_type VARCHAR(50) NOT NULL,
    amount INT DEFAULT 0,
    message TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Messages
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sender_id UUID REFERENCES users(id) ON DELETE CASCADE,
    receiver_id UUID REFERENCES users(id) ON DELETE CASCADE,
    idea_id UUID REFERENCES ideas(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Notifications
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    related_id UUID,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Reports
CREATE TABLE IF NOT EXISTS reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reporter_id UUID REFERENCES users(id) ON DELETE SET NULL,
    target_type VARCHAR(50) NOT NULL,
    target_id UUID NOT NULL,
    reason TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

NOTIFY pgrst, 'reload schema';
"""

try:
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("Migration successful! Tables created.")
    cur.close()
    conn.close()
except Exception as e:
    print("Migration failed:", e)
