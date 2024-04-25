/** @odoo-module */

import { registry } from "@web/core/registry";
import { getDefaultConfig } from "@web/views/view";
import { useService } from "@web/core/utils/hooks"
const { Component, onWillStart, useSubEnv, useState } = owl;

export class reviewPaymenttodayReport1 extends Component {

    setup() {
//  display: none;
        this.state = useState({
        Data:[],
        should_show:true,
        show_name_company:'',
        select_partner_id:  0,
        from_date: 'YYYY-MM-DD',
        to_date: 'YYYY-MM-DD',
        viewreport:'date',
        view_open:false,
        show_product:false,
        // user_id:0,
        show_name_analysis:'',
        show_name_categ:'',
        select_analysis_acc_id:0,
        select_saleman_id:0,
        selcect_journal_id:0,
        hide_payment_cancel:false,
        filter_list:[],
        page:1,
        size_page:1,
        par_id:0,
        accou_id:0
        });
        this.options={}
        this.analysis={}
        this.salesman={}
        this.journals={}
        this.orm = useService("orm")
        this.actionService = useService("action")
        this.user_id=0
        this.move_state='posted';
        
        onWillStart(async () => {
            console.log("ww")
            await this.getAcconts()
            await this.load()
    
        });
    }
    async getAcconts(){
      const model = "paytoday.redys";
      const domain = [];
      const fields = [];
      const method="get_accounts_report"
      const records = await  this.orm.call(model,method)
      records.forEach(element => {
        this.options=element.partner_list
        this.salesman=element.saleman_list
        this.analysis=element.analysis_account_list
        this.journals=element.journal_ids_list
      });
        
      
      console.log(this.options)
      console.log(this.salesman)
    }
    async load(){
        let model = "paytoday.redys";
        let domain=[]
        let fields = [];
        let filter=[]
        let method="process_data_report_payment"
        let records = await  this.orm.call(model,method)
        filter.push(records);
        this.state.filter_list=filter      
        if(records.length==0){
          console.log(records)
        }
        else{
          console.log(records)
          if(records.partner_id ){
            this.state.select_partner_id=records.partner_id
          }
          if(records.analysis_account_id ){
            this.state.select_analysis_acc_id=records.analysis_account_id
           
          }
          // if(records.journal_id ){
          //   this.state.selcect_journal_id=records.journal_id
          // }
          if(records.salesman_id ){
            this.state.select_saleman_id=records.salesman_id
          }
          console.log(records.from_date )
          if(records.from_date!=undefined){
            this.state.from_date=records.from_date
          }
          console.log(records.to_date )
          if(records.to_date!=undefined){
            this.state.to_date=records.to_date
          }
          if(records.order_view!=undefined){
            this.state.viewreport=records.order_view
          }
         
          if(records.hide_payment_cancel!=undefined){
            this.state.hide_payment_cancel=records.hide_payment_cancel
          }
          
        }

        console.log(this.state.Data,"data1")

        this.state.Data=await this.getData(this.state.filter_list)
        this.state.show_product=this.state.Data.show_product
        this.state.show_name_analysis=this.state.Data.show_product
        this.state.show_name_categ=this.state.Data.show_product

        console.log(this.state.Data,"data2")
      }
     async updateData_after() {
        this.state.show_name_analysis=''
        let Filter_data_after=[{
            'partner_id': parseInt(this.state.select_partner_id),
            'salesman_id': parseInt(this.state.select_saleman_id),
            'from_date':this.state.from_date  ,
            'to_date': this.state.to_date,
            'product_id': false,
            'pro_cate_id':false,
            'product_type':'product',
            'analysis_account_id': parseInt(this.state.select_analysis_acc_id),
            'company_ids': false,
            'hide_payment_cancel': this.state.hide_payment_cancel,
            'type_payment': 'all',
            'show_payment_this_company':false,
            'order_view':this.state.viewreport,
            // 'user_id':parseInt(this.user_id),
           
            'journal_id':parseInt(this.state.selcect_journal_id),
        }]
        console.log(Filter_data_after)
        this.state.filter_list=Filter_data_after
        this.state.Data=await this.getData(Filter_data_after)
        this.state.show_product=this.state.Data.show_product
        this.state.show_name_analysis=this.state.Data.show_product
        this.state.show_name_categ=this.state.Data.show_product
      }
      async getData(Filter_data) {
        console.log(this.state.filter_list,"filter")
        console.log('GET')
        let model = "paytoday.redys";
        let domain=Filter_data
        let fields = [];
        let method="get_report_payment"
       
        let records = await  this.orm.call(model,method,domain)
        console.log('GET2')
       
      
      console.log(records,"records")
      return records
     }
    
     
      async _onClickViewDetail(ev) {
        let detailId = $(ev.currentTarget).data('detail-id');
        console.log('Detail ID:', detailId);
        let model = "account.move";
        let domain=[['id', '=',  detailId]]
        let fields = [];
        let method="open_action_report"
        var action = await  this.orm.call(model,method,domain)
        this.actionService.doAction(action)
    
      }
}

reviewPaymenttodayReport1.template = "yousentech_sale_reports.dy_report_review_payment_today_temp1";
reviewPaymenttodayReport1.events={
    
  "click .view-detail": "_onClickViewDetail",



}
registry.category("actions").add("yousentech_sale_reports.paytoday_re", reviewPaymenttodayReport1);
