from datetime import datetime
import json
from django.shortcuts import render, redirect, HttpResponse
from . models import *
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from web3 import Web3


#######################################################################################################
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
print("Ganache Web3 Connected:",web3.isConnected(),"\n")

web3.eth.defaultAccount = web3.eth.accounts[0]

abi = json.loads("""[
	{
		"constant": false,
		"inputs": [
			{
				"name": "_docsid",
				"type": "uint256"
			},
			{
				"name": "_userid",
				"type": "uint256"
			},
			{
				"name": "_amount",
				"type": "string"
			},
			{
				"name": "_paymentscreenshot",
				"type": "string"
			},
			{
				"name": "_status",
				"type": "string"
			}
		],
		"name": "addDocument",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "count_documents",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "get_Document_transactions",
		"outputs": [
			{
				"name": "",
				"type": "uint256[]"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "_docsid",
				"type": "uint256"
			}
		],
		"name": "getDocument",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "string"
			},
			{
				"name": "",
				"type": "string"
			},
			{
				"name": "",
				"type": "string"
			},
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	}
]""")

bytecode =  "608060405234801561001057600080fd5b506107cd806100206000396000f300608060405260043610610062576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff16806328bfe801146100675780633f9b250a146100d357806372975f471461025f578063cd6ad63a1461028a575b600080fd5b34801561007357600080fd5b5061007c610393565b6040518080602001828103825283818151815260200191508051906020019060200280838360005b838110156100bf5780820151818401526020810190506100a4565b505050509050019250505060405180910390f35b3480156100df57600080fd5b506100fe600480360381019080803590602001909291905050506103eb565b60405180868152602001806020018060200180602001858152602001848103845288818151815260200191508051906020019080838360005b83811015610152578082015181840152602081019050610137565b50505050905090810190601f16801561017f5780820380516001836020036101000a031916815260200191505b50848103835287818151815260200191508051906020019080838360005b838110156101b857808201518184015260208101905061019d565b50505050905090810190601f1680156101e55780820380516001836020036101000a031916815260200191505b50848103825286818151815260200191508051906020019080838360005b8381101561021e578082015181840152602081019050610203565b50505050905090810190601f16801561024b5780820380516001836020036101000a031916815260200191505b509850505050505050505060405180910390f35b34801561026b57600080fd5b50610274610646565b6040518082815260200191505060405180910390f35b34801561029657600080fd5b506103916004803603810190808035906020019092919080359060200190929190803590602001908201803590602001908080601f0160208091040260200160405190810160405280939291908181526020018383808284378201915050505050509192919290803590602001908201803590602001908080601f0160208091040260200160405190810160405280939291908181526020018383808284378201915050505050509192919290803590602001908201803590602001908080601f0160208091040260200160405190810160405280939291908181526020018383808284378201915050505050509192919290505050610653565b005b606060018054806020026020016040519081016040528092919081815260200182805480156103e157602002820191906000526020600020905b8154815260200190600101908083116103cd575b5050505050905090565b600060608060606000806000878152602001908152602001600020600101546000808881526020019081526020016000206002016000808981526020019081526020016000206003016000808a81526020019081526020016000206004016000808b815260200190815260200160002060050154838054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156104f45780601f106104c9576101008083540402835291602001916104f4565b820191906000526020600020905b8154815290600101906020018083116104d757829003601f168201915b50505050509350828054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156105905780601f1061056557610100808354040283529160200191610590565b820191906000526020600020905b81548152906001019060200180831161057357829003601f168201915b50505050509250818054600181600116156101000203166002900480601f01602080910402602001604051908101604052809291908181526020018280546001816001161561010002031660029004801561062c5780601f106106015761010080835404028352916020019161062c565b820191906000526020600020905b81548152906001019060200180831161060f57829003601f168201915b505050505091509450945094509450945091939590929450565b6000600180549050905090565b600080600087815260200190815260200160002090508481600101819055508381600201908051906020019061068a9291906106fc565b50828160030190805190602001906106a39291906106fc565b50818160040190805190602001906106bc9291906106fc565b5042816005018190555060018087908060018154018082558091505090600182039060005260206000200160009091929091909150555050505050505050565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f1061073d57805160ff191683800117855561076b565b8280016001018555821561076b579182015b8281111561076a57825182559160200191906001019061074f565b5b509050610778919061077c565b5090565b61079e91905b8082111561079a576000816000905550600101610782565b5090565b905600a165627a7a723058209bc5b3bcf68f9970907891b4e7b1ea1f7632782a855bb98af0c0a1aafc2ba3230029"

# news_sol = web3.eth.contract(abi=abi,bytecode=bytecode)

contract = web3.eth.contract(address="0xdedeAA05b0E57237700C5F11Fa5E697FE7bA3889",abi=abi)

############################################### ipfs ##########################################################
import ipfshttpclient
ipfsconnection = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')

########################################## view function ######################################################

class convertobjectbystatement: 
    def __init__(self, tid, uid, amount, screenshot, status, timestamp, username, phone, email):
        self.tid = tid
        self.uid = uid
        self.amount = amount
        self.screenshot = screenshot
        self.status = status
        self.timestamp = timestamp
        self.username = username
        self.phone = phone
        self.email  = email

# Create your views here.
def userloginpage(request):
    return render(request,'user_login.html')

def usersignuppage(request):
    return render(request,'user_signup.html')

def usersignup(request):
    if request.method == "POST":
        name = request.POST['username']
        ph = request.POST['phone']
        mail = request.POST['email']
        pwd = request.POST['password']

        try: 
            usignup = user(username=name,phone=ph,email=mail,account='',password=pwd)
            usignup.save()
            messages.info(request,'Successfully Registered')
            return redirect('userloginpage')

        except:
            messages.info(request,'something went wrong try again')
            return redirect('userloginpage')
    
    return redirect('userloginpage')

def userlogin(request):
    if request.method == "POST":
        mail = request.POST['email']
        pwd = request.POST['password']

        try: 
            u = user.objects.get(email=mail, password=pwd)
            request.session['uid'] = u.id
            request.session['uname'] = u.username
            return redirect('userhome')
        except:
            messages.info(request,'Email or Password are invalid')
            return redirect('userloginpage')
    
    return redirect('userloginpage')

def userlogout(request):
    request.session['uid'] = None
    return redirect('userloginpage')

def userhome(request):
    uid = request.session['uid']
    if uid != None:
        username = request.session['uname'] 
        return render(request,'user_home.html',{'username':username})
    else:
        messages.info(request,'Something went worng please login again')
        return redirect('userloginpage')

def userdonatepage(request):
    uid = request.session['uid']
    if uid != None:
        return render(request,'user_donate.html')
    else:
        messages.info(request,'Something went worng please login again')
        return redirect('userloginpage')

def userdonate(request):
    uid = request.session['uid']
    if uid != None:
        if request.method == "POST":
            amount = request.POST['amount']
            screenshot = request.FILES['screenshot']
            uid = request.session['uid'] 
            state = statement(amount=amount,screenshot=screenshot,status="pending",uid=uid)
            state.save()
        messages.info(request,'Successfully Donated, Thank You')
        return render(request,'user_donate.html')
    else:
        messages.info(request,'Something went worng please login again')
        return redirect('userloginpage')

def userpendingpage(request):
    uid = request.session['uid']
    if uid != None:
        try:
            uid = request.session['uid']
            state = statement.objects.filter(uid=uid, status='pending')
            print(state)
            return render(request,'user_pending_statement.html',{'state': state})
        except:
            messages.info(request,'data not found')
            return render(request,'user_pending_statement.html')
    else:
        messages.info(request,'Something went worng please login again')
        return redirect('userloginpage')

def userapporvedpage(request):
    uid = request.session['uid']
    if uid != None:
        got = []
        total = contract.functions.get_Document_transactions().call()
        total = list(set(total))
        for i in range(0, len(total)):
            x = contract.functions.getDocument(int(total[i])).call()
            dt_obj = datetime.fromtimestamp(x[4])
            u = user.objects.get(id=x[0])
            if x[3] == "approved" and x[0] == uid:
                got.append(convertobjectbystatement(int(total[i]),x[0],x[1],x[2],x[3],dt_obj,u.username,u.phone,u.email))
        print(got)
        return render(request,'user_approved_statement.html',{'statement':got})
    else:
        messages.info(request,'Something went worng please login again')
        return redirect('userloginpage')

def userrejectedpage(request):
    uid = request.session['uid']
    if uid != None:
        got = []
        total = contract.functions.get_Document_transactions().call()
        total = list(set(total))
        for i in range(0, len(total)):
            x = contract.functions.getDocument(int(total[i])).call()
            dt_obj = datetime.fromtimestamp(x[4])
            u = user.objects.get(id=x[0])
            if x[3] == "rejected" and x[0] == uid:
                got.append(convertobjectbystatement(int(total[i]),x[0],x[1],x[2],x[3],dt_obj,u.username,u.phone,u.email))
        print(got)
        return render(request,'user_rejected_statement.html',{'statement':got})
    else:
        messages.info(request,'Something went worng please login again')
        return redirect('userloginpage')

#======================================== admin =======================================
def adminloginpage(request):
    return render(request,'admin_login.html')
    
def adminlogin(request):
    if request.method == "POST":
        mail = request.POST['email']
        pwd = request.POST['password']

        if mail=="admin@gmail.com" and pwd=="admin":
            request.session['aid'] = '0'
            return redirect('adminhomepage')
        else:
            messages.info(request,'Email or Password are invalid')
            return redirect('adminloginpage')

    return redirect('adminloginpage')

def adminlogout(request):
    request.session['aid'] = None
    return redirect('adminloginpage')

def adminhomepage(request):
    aid = request.session['aid']
    if aid != None:
        return render(request,'admin_home.html',{'username':'Admin'})
    else:
        messages.info(request,'Something went worng please login again')
        return redirect('adminloginpage')

def adminpendingpage(request):
    aid = request.session['aid']
    if aid != None:
        try:
            state = statement.objects.filter(status='pending')
            usr = user.objects.all()
            return render(request,'admin_pending_statement.html',{'state': state,'usr': usr})
        except:
            messages.info(request,'data not found')
            return render(request,'admin_pending_statement.html')
    else:
        messages.info(request,'Something went worng please login again')
        return redirect('adminloginpage')

def adminrejectedpage(request):
    aid = request.session['aid']
    if aid != None:
        return render(request,'admin_rejected_statement.html')
    else:
        messages.info(request,'Something went worng please login again')
        return redirect('adminloginpage')

def adminapporve(request,uid,sid):
    aid = request.session['aid']
    if aid != None:
        print(uid, sid)
        s=statement.objects.get(id=sid)
        res = ipfsconnection.add(s.screenshot)
        print("IPFS Img stored hash",res['Hash'])
        count = contract.functions.count_documents().call()
        transaction_hash = contract.functions.addDocument(count+1,uid,s.amount,res['Hash'],"approved").transact({'from': web3.eth.accounts[0]})
        receipt = web3.eth.waitForTransactionReceipt(transaction_hash)
        print("Used Eth for gas:",(receipt.gasUsed*0.00000002),"\n")
        statement.objects.filter(id=sid).update(status="approved")
        messages.info(request,'Transaction Done')
        return redirect('adminpendingpage')
    else:
        messages.info(request,'Something went worng please login again')
        return redirect('adminloginpage')

def adminreject(request,uid,sid):
    aid = request.session['aid']
    if aid != None:
        print(uid, sid)
        s=statement.objects.get(id=sid)
        res = ipfsconnection.add(s.screenshot)
        print("IPFS Img stored hash",res['Hash'])
        count = contract.functions.count_documents().call()
        transaction_hash = contract.functions.addDocument(count+1,uid,s.amount,res['Hash'],"rejected").transact({'from': web3.eth.accounts[0]})
        receipt = web3.eth.waitForTransactionReceipt(transaction_hash)
        print("Used Eth for gas:",(receipt.gasUsed*0.00000002),"\n")
        statement.objects.filter(id=sid).update(status="rejected")
        messages.info(request,'Transaction Done')
        return redirect('adminpendingpage')
    else:
        messages.info(request,'Something went worng please login again')
        return redirect('adminloginpage')

def adminapporvedpage(request):
    aid = request.session['aid']
    if aid != None:
        got = []
        total = contract.functions.get_Document_transactions().call()
        total = list(set(total))
        for i in range(0, len(total)):
            x = contract.functions.getDocument(int(total[i])).call()
            dt_obj = datetime.fromtimestamp(x[4])
            u = user.objects.get(id=x[0])
            if x[3] == "approved":
                got.append(convertobjectbystatement(int(total[i]),x[0],x[1],x[2],x[3],dt_obj,u.username,u.phone,u.email))
        print(got)
        return render(request,'admin_approved_statement.html',{'statement':got})
    else:
        messages.info(request,'Something went worng please login again')
        return redirect('adminloginpage')

def adminrejectedpage(request):
    aid = request.session['aid']
    if aid != None:
        got = []
        total = contract.functions.get_Document_transactions().call()
        total = list(set(total))
        for i in range(0, len(total)):
            x = contract.functions.getDocument(int(total[i])).call()
            dt_obj = datetime.fromtimestamp(x[4])
            u = user.objects.get(id=x[0])
            if x[3] == "rejected":
                got.append(convertobjectbystatement(int(total[i]),x[0],x[1],x[2],x[3],dt_obj,u.username,u.phone,u.email))
        print(got)
        return render(request,'admin_rejected_statement.html',{'statement':got})
    else:
        messages.info(request,'Something went worng please login again')
        return redirect('adminloginpage')