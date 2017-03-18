# TODO: parameterise the publish

publish_dashboard:
	rm -rf ./publish/configure_dashboard/
	mkdir -p ./publish/configure_dashboard
	cp -r ./configure_dashboard ./publish/
	pip install -t ./publish/configure_dashboard -r ./publish/configure_dashboard/requirements.txt
	cd ./publish/configure_dashboard && zip -r ../configure_dashboard.zip .

publish_curator:
	rm -rf ./publish/curator_lambda/
	mkdir -p ./publish/curator_lambda
	cp -r ./curator_lambda ./publish/
	pip install -t ./publish/curator_lambda -r ./publish/curator_lambda/requirements.txt
	cd ./publish/curator_lambda && zip -r ../curator_lambda.zip .

publish_streamer:
	rm -rf ./publish/cwlogs-streamer/
	mkdir -p ./publish/cwlogs-streamer
	cp -r ./cwlogs-streamer ./publish/
	cd ./publish/cwlogs-streamer && zip -r ../cwlogs-streamer.zip .

clean:
	@echo "--> Cleaning pyc files"
	find . -name "*.pyc" -delete
	rm -rf ./publish
	@echo ""
