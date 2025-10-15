# Waskita - Makefile untuk Docker Management
# Minimal Setup - Simplified Configuration

.PHONY: help fresh-build build clean status logs restart stop

help: ## Tampilkan bantuan
	@echo "Waskita - Docker Management Commands"
	@echo "===================================="
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""

fresh-build: ## Fresh build dengan menghapus semua data dan membuat sample data
	@echo "🔥 Starting fresh build..."
	@echo "⚠️  WARNING: This will DELETE ALL existing data!"
	@echo ""
	docker-compose down --volumes --remove-orphans
	docker volume rm waskita_postgres_data -f 2>/dev/null || true
	CREATE_SAMPLE_DATA=true docker-compose up --build -d
	@echo ""
	@echo "✅ Fresh build completed!"
	@echo "🌐 Access: http://localhost:5000"
	@echo "🔐 Admin: admin / admin123"
	@echo "👤 User: testuser / testuser123"

build: ## Normal build dengan data persistent
	@echo "🛠️  Starting normal build..."
	docker-compose up --build -d
	@echo ""
	@echo "✅ Build completed!"
	@echo "🌐 Access: http://localhost:5000"

clean: ## Hapus semua container dan volume
	@echo "🧹 Cleaning up..."
	docker-compose down --volumes --remove-orphans
	docker volume rm waskita_postgres_data -f 2>/dev/null || true
	docker system prune -f
	@echo "✅ Cleanup completed!"

status: ## Tampilkan status container
	@echo "📊 Container Status:"
	@docker-compose ps

logs: ## Tampilkan logs aplikasi
	@echo "📋 Application Logs:"
	@docker-compose logs -f web

restart: ## Restart services
	@echo "🔄 Restarting services..."
	docker-compose restart
	@echo "✅ Services restarted!"

stop: ## Stop semua services
	@echo "⏹️  Stopping all services..."
	docker-compose down
	@echo "✅ All services stopped!"