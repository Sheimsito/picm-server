#!/usr/bin/env bash
# Exit on any error
set -o errexit

echo "🚀 Starting build process..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run Django migrations
echo "🔄 Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo "👤 Creating admin user..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@picm.com', 'admin123')
    print('✅ Admin user created: admin / admin123')
else:
    print('ℹ️  Admin user already exists')
EOF

echo "✅ Build completed successfully!"
