build: 
	docker build -t car-price-prediction-service:v1 .
	
install: build
	pip install pip --upgrade
	pip install pyopenssl --upgrade
	pip install awsebcli

deploy: build install
	eb init -p docker -r us-east-1 car-price-pred-app
	eb create car-price-env