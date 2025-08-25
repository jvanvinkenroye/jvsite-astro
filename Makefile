PY?=python3
PELICAN?=pelican
PELICAN_OPTS?=

BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
CONFFILE=$(BASEDIR)/pelicanconf.py

DEBUG ?= 0
ifeq ($(DEBUG), 1)
	PELICAN_OPTS += -D
endif

RELATIVE ?= 0
ifeq ($(RELATIVE), 1)
	PELICAN_OPTS += --relative-urls
endif

SERVER ?= "0.0.0.0"
PORT ?= 0
ifneq ($(PORT), 0)
	PELICAN_OPTS += -p $(PORT)
endif

help:
	@echo 'Makefile for a Pelican Web site'
	@echo ''
	@echo 'Usage:'
	@echo '   make setup           install dependencies'
	@echo '   make html            (re)generate the web site'
	@echo '   make clean           remove the generated files'
	@echo '   make serve           serve site at http://localhost:8000'
	@echo '   make devserver       serve and regenerate files automatically'
	@echo ''

setup:
	@echo "📦 Setting up Pelican environment..."
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt
	@echo "✅ Setup complete!"

html:
	@echo "🏗️  Generating site..."
	./venv/bin/$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICAN_OPTS)
	@echo "✅ Site generated in $(OUTPUTDIR)"

clean:
	[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)

serve:
ifdef PORT
	cd $(OUTPUTDIR) && $(PY) -m http.server $(PORT)
else
	cd $(OUTPUTDIR) && $(PY) -m http.server 8000
endif

devserver:
	@echo "🚀 Starting development server at http://localhost:8000"
	./venv/bin/$(PELICAN) --autoreload --listen $(PELICAN_OPTS)

.PHONY: html help clean serve devserver setup