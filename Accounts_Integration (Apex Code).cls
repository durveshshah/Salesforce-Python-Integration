@RestResource(urlMapping='/v1/accounts/*')
global with sharing class Accounts_Integration{


private class Attach {
    String Body;
    String ContentType;
    String Name;
}
private class AccountClass {
    Account thisAccount;
    list<Attach> attachments;
} 

    @HttpGet
    global static void doGet() {
        String result = '';
        RestRequest request = RestContext.request;
        List<Account> acclist = [Select Id,phone,AccountNumber,Name,createddate,Created_Date_New__c,(select id from attachments) from Account order by createddate desc];
        if( acclist.size() > 0 ) {
            Map<String,List<Account>> resultMap = new Map<String,List<Account>>();

            resultMap.put('accountId',acclist);

            result = JSON.serialize( resultMap );
        } else {
            result = ' No Account ID found!';
        }

        RestContext.response.addHeader('Content-Type','application/json');
        RestContext.response.responseBody = Blob.valueOf(result);
    }

    @HttpPost
   global static String doPost() 
        {
        
        AccountClass container = (AccountClass)System.JSON.deserialize(
        RestContext.request.requestBody.tostring(), 
        AccountClass.class);
        
        Account account = container.thisAccount;
        
        insert account;
     

      list<attachment> attachmentToInsert = new list<attachment>();
      for (Attach att :container.attachments) {
      
      if(att.body != null)
      {
        attachmentToInsert.add(
            new Attachment(parentId = account.Id, name = att.name, 
                           Body = EncodingUtil.base64Decode(att.body)));
     

     }
     
     
   
     } 
     
         insert attachmentToInsert; 
       return account.id;
        
            
    }
}