pragma solidity ^0.4.25;
  
contract NGO{
  
    // Document

   struct Document{
       uint docsid; //-1
       uint userid; //0
       string amount; //1
       string paymentscreenshot; //2
       string status; //3
       uint timestamp; //4
   }

    mapping (uint => Document) Documents;
    uint[] Document_details;

    function get_Document_transactions() view public returns (uint[]){
        return Document_details;
    }
    
    function count_documents() view  public returns (uint) {
        return Document_details.length;
    }

    function addDocument(uint _docsid, uint _userid, string _amount, string _paymentscreenshot, string _status) public{
        var Document = Documents[_docsid];
        Document.userid = _userid;
        Document.amount = _amount;
        Document.paymentscreenshot = _paymentscreenshot;
        Document.status = _status;
        Document.timestamp = now;
        
        Document_details.push(_docsid)-1;
    }
    
    function getDocument(uint _docsid) view public returns (uint,string memory,string memory,string memory,uint){
        return(Documents[_docsid].userid,Documents[_docsid].amount,Documents[_docsid].paymentscreenshot,Documents[_docsid].status,Documents[_docsid].timestamp);
    }

}