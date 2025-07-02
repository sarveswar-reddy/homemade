from flask import Flask, request, render_template, redirect, url_for
import boto3
import uuid

app = Flask(__name__)

# AWS clients using IAM role (EC2 attached)
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
sns = boto3.client('sns', region_name='ap-south-1')

# DynamoDB table and SNS topic
order_table = dynamodb.Table('PickleOrders')
SNS_TOPIC_ARN = 'arn:aws:sns:ap-south-1:123456789012:OrderConfirmations'  # Replace with your SNS ARN

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        name = request.form['name']
        item = request.form['item']
        quantity = int(request.form['quantity'])
        order_id = str(uuid.uuid4())

        # Save to DynamoDB
        order_table.put_item(Item={
            'order_id': order_id,
            'name': name,
            'item': item,
            'quantity': quantity
        })

        return redirect(url_for('sucess'))
    return render_template('order.html')

@app.route('/notify')
def notify():
    # Send a sample SNS message
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message='A new order was received on Homemade Pickles & Snacks!',
        Subject='New Pickle Order Alert'
    )
    return "SNS notification sent!"

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        return redirect(url_for('sucess'))
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('sucess'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return redirect(url_for('sucess'))
    return render_template('signup.html')

@app.route('/sucess')
def sucess():
    return render_template('sucess.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        return redirect(url_for('sucess'))
    return render_template('checkout.html')

@app.route('/snackes')
def snackes():
    return render_template('snackes.html')

@app.route('/veg_pickles')
def veg_pickles():
    return render_template('veg_pickles.html')

@app.route('/non_veg_pickles')
def non_veg_pickles():
    return render_template('non_veg_pickles.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)