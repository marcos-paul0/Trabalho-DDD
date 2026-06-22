#!/bin/bash
# Script de inicialização do projeto Media Vault

set -e

echo "🎬 Media Vault - Inicialização do Projeto"
echo "=========================================="
echo ""

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Função para imprimir mensagens coloridas
print_info() {
    echo -e "${BLUE}ℹ ${1}${NC}"
}

print_success() {
    echo -e "${GREEN}✓ ${1}${NC}"
}

print_warning() {
    echo -e "${YELLOW}! ${1}${NC}"
}

# Verificar dependências
check_dependencies() {
    print_info "Verificando dependências..."
    
    if ! command -v python3 &> /dev/null; then
        print_warning "Python 3 não encontrado. Instale Python 3.10+"
        exit 1
    fi
    print_success "Python 3 encontrado"
    
    if ! command -v node &> /dev/null; then
        print_warning "Node.js não encontrado. Instale Node.js 16+"
        exit 1
    fi
    print_success "Node.js encontrado"
    
    if ! command -v docker &> /dev/null; then
        print_warning "Docker não encontrado (opcional para dev)"
    else
        print_success "Docker encontrado"
    fi
}

# Setup Backend
setup_backend() {
    echo ""
    print_info "Configurando Backend (Django)..."
    
    cd backend
    
    # Criar venv
    if [ ! -d "venv" ]; then
        print_info "Criando ambiente virtual..."
        python3 -m venv venv
        print_success "Ambiente virtual criado"
    fi
    
    # Ativar venv
    source venv/bin/activate
    
    # Instalar dependências
    print_info "Instalando dependências Python..."
    pip install -q -r requirements.txt
    print_success "Dependências instaladas"
    
    # Configurar .env
    if [ ! -f ".env" ]; then
        print_info "Criando arquivo .env..."
        cp .env.example .env
        print_warning "Edite o arquivo backend/.env conforme necessário"
    fi
    
    # Migrations
    print_info "Executando migrations..."
    python manage.py migrate -q
    print_success "Migrations executadas"
    
    # Criar superusuário
    print_warning "Você precisa criar um superusuário agora:"
    python manage.py createsuperuser
    
    cd ..
}

# Setup Frontend
setup_frontend() {
    echo ""
    print_info "Configurando Frontend (React)..."
    
    cd frontend
    
    print_info "Instalando dependências..."
    npm install -q
    print_success "Dependências instaladas"
    
    cd ..
}

# Main
main() {
    check_dependencies
    
    echo ""
    echo "Selecione a opção:"
    echo "1) Setup Completo (Backend + Frontend)"
    echo "2) Setup Backend apenas"
    echo "3) Setup Frontend apenas"
    echo "4) Usar Docker Compose"
    echo ""
    read -p "Escolha [1-4]: " choice
    
    case $choice in
        1)
            setup_backend
            setup_frontend
            echo ""
            print_success "Setup completo finalizado!"
            echo ""
            echo "Para iniciar o projeto:"
            echo "  Terminal 1 - Backend:"
            echo "    cd backend && source venv/bin/activate && python manage.py runserver"
            echo ""
            echo "  Terminal 2 - Frontend:"
            echo "    cd frontend && npm start"
            echo ""
            ;;
        2)
            setup_backend
            print_success "Setup Backend finalizado!"
            ;;
        3)
            setup_frontend
            print_success "Setup Frontend finalizado!"
            ;;
        4)
            print_info "Iniciando com Docker Compose..."
            docker-compose -f docker/docker-compose.yml up -d
            print_success "Docker Compose iniciado!"
            echo ""
            echo "Acesse:"
            echo "  - Frontend: http://localhost:3000"
            echo "  - Backend: http://localhost:8000"
            echo "  - Admin: http://localhost:8000/admin"
            echo ""
            ;;
        *)
            print_warning "Opção inválida"
            exit 1
            ;;
    esac
}

main
