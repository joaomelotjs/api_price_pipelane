cat > check.sh << 'EOF'
#!/bin/bash
echo "=== Checando ambiente ==="
python -c "import streamlit; import sqlalchemy; print('✅ Dependências ok')"
cat .env > /dev/null && echo "✅ .env existe" || echo "❌ .env não encontrado"
python -c "from app.database.connection import test_connection; test_connection(); print('✅ Banco conectado')"
EOF
chmod +x check.sh