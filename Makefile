# Run celery
.PHONY: run-celery
run-celery:
	@echo "Running celery..."
	@celery -A config.settings.celery worker -l INFO

# Clean up migration files
.PHONY: clean-migrations
clean-migrations:
	@echo "Cleaning up migration files..."
	@find core -path "*/migrations/*.py" -not -name "__init__.py" -delete
	@find core -path "*/migrations/*.pyc" -delete

# Collect static files
.PHONY: collectstatic
collectstatic:
	@echo "Collecting static files..."
	@python manage.py collectstatic --noinput

# Flush the database (removes all data and resets it)
.PHONY: flush
flush: 
	@echo "Flushing the database..."
	@python manage.py flush

# Generate API schema
.PHONY: generate-schema
generate-schema:
	@echo "Generating API schema..."
	@python manage.py spectacular --color --file schema.yml

# Install all dependencies (production and development)
.PHONY: install-all-requirements
install-all-requirements:
	@echo "Installing all dependencies (production and development)..."
	@pip install -r requirements/base.txt -r requirements/local.txt

# Install and configure pre-commit hooks
.PHONY: install-pre-commit
install-pre-commit:
	@echo "Installing and configuring pre-commit hooks..."
	@pre-commit uninstall
	@pre-commit install

# Install production dependencies
.PHONY: install-production-requirements
install-production-requirements:
	@echo "Installing production dependencies..."
	@pip install -r requirements/base.txt

# Run linters
.PHONY: lint
lint:
	@echo "Running linters..."
	@pre-commit run --all-files

# Create migration files
.PHONY: migrations
migrations:
	@echo "Creating migration files..."
	@python manage.py makemigrations

# Apply tenant-specific migrations
.PHONY: migrate_tenant
migrate_tenant:
	@echo "Applying tenant-specific migrations..."
	@python manage.py migrate_schemas

# Apply shared migrations
.PHONY: migrate_shared
migrate_shared:
	@echo "Applying shared migrations..."
	@python manage.py migrate_schemas --shared
	
# Run the development server
.PHONY: run-server
run-server:
	@echo "Running the development server..."
	@python manage.py runserver

# Open the Django shell
.PHONY: shell
shell:
	@echo "Opening the Django shell..."
	@python manage.py shell

# Create a superuser
.PHONY: superuser
superuser:
	@echo "Creating a superuser..."
	@python manage.py createsuperuser

# Run tailwind
.PHONY: run-tailwind
run-tailwind:
	@echo "Running tailwind..."
	@python manage.py tailwind start  

# Update project (install dependencies, apply migrations, install pre-commit hooks)
.PHONY: update
update: install-all-requirements migrate install-pre-commit
	@echo "Updating project..."
