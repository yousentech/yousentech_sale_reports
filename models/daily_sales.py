from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta, date
import calendar
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
import json
import os
class report_dailysales(models.TransientModel):
    _name='paytoday.redys'
    _description = 'Search_Review_'
      
    partner_id=fields.Many2one('res.partner',string="Partner" 
        
    )
    salesman_id=fields.Many2one('salesman',string="Salesman" 
    )
    # journal_id = fields.Many2one('account.journal',string="دفتر اليومية" ,)
    
    from_date = fields.Date(
        string='From Date',
        
    )
    to_date = fields.Date(
        string='To Date',  
    )
    analysis_account_id = fields.Many2one('account.analytic.account',string="Analytic Account" 
    )
    
    def _get_company(self):
        user_id=self.env.user
        return [('id','in',user_id.company_ids.ids)]
    company_ids = fields.Many2one('res.company',
        string='Company',  
        domain=_get_company,   
        
    )
    user_id=fields.Many2one('res.users',string="User Name" ,
                            default=lambda self: self.env.user,
                            readonly=True                     
    )
    type_payment = fields.Selection(
        [('out_refund', 'Refund')
        ,('out_invoice', 'Invoice'),
         
       ],
         string='Report Type', 
    )
    # order_view=fields.Selection(
    #     [("product","حسب الصنف"),("invoice","حسب الفاتورة")],
    #     string='عرض التقارير',
    #     default="invoice"
    # )
    hide_payment_cancel=fields.Boolean(
        string='Hide Canceled Sales',
        default=True
        
    )
    date_range = fields.Selection(
        [('today', 'Today'),
         ('this_week', 'This Week'),
         ('this_month', 'This Month'),
         ('this_quarter', 'This Quarter'),
         ('this_financial_year', 'This financial Year'),
         ('yesterday', 'Yesterday'),
         ('last_week', 'Last Week'),
         ('last_month', 'Last Month'),
         ('last_quarter', 'Last Quarter'),
         ('last_financial_year', 'Last Financial Year')],
        string='Period of Time', default='this_financial_year'
    )
    @api.onchange('date_range')
    def onchange_date_range(self):
        if self.date_range:
            date = datetime.today()
            if self.date_range == 'today':
                self.from_date = date.strftime("%Y-%m-%d")
                self.to_date = date.strftime("%Y-%m-%d")
            if self.date_range == 'this_week':
                day_today = date - timedelta(days=date.weekday())
                self.from_date = (day_today - timedelta(days=date.weekday())).strftime("%Y-%m-%d")
                self.to_date = (day_today + timedelta(days=6)).strftime("%Y-%m-%d")
            if self.date_range == 'this_month':
                self.from_date = datetime(date.year, date.month, 1).strftime("%Y-%m-%d")
                self.to_date = datetime(date.year, date.month, calendar.mdays[date.month]).strftime("%Y-%m-%d")
            if self.date_range == 'this_quarter':
                if int((date.month - 1) / 3) == 0:  # First quarter
                    self.from_date = datetime(date.year, 1, 1).strftime("%Y-%m-%d")
                    self.to_date = datetime(date.year, 3, calendar.mdays[3]).strftime("%Y-%m-%d")
                if int((date.month - 1) / 3) == 1:  # Second quarter
                    self.from_date = datetime(date.year, 4, 1).strftime("%Y-%m-%d")
                    self.to_date = datetime(date.year, 6, calendar.mdays[6]).strftime("%Y-%m-%d")
                if int((date.month - 1) / 3) == 2:  # Third quarter
                    self.from_date = datetime(date.year, 7, 1).strftime("%Y-%m-%d")
                    self.to_date = datetime(date.year, 9, calendar.mdays[9]).strftime("%Y-%m-%d")
                if int((date.month - 1) / 3) == 3:  # Fourth quarter
                    self.from_date = datetime(date.year, 10, 1).strftime("%Y-%m-%d")
                    self.to_date = datetime(date.year, 12, calendar.mdays[12]).strftime("%Y-%m-%d")
            if self.date_range == 'this_financial_year':
                    self.from_date = datetime(date.year, 1, 1).strftime("%Y-%m-%d")
                    self.to_date = datetime(date.year, 12, 31).strftime("%Y-%m-%d")
                
            date = (datetime.now() - relativedelta(days=1))
            if self.date_range == 'yesterday':
                self.from_date = date.strftime("%Y-%m-%d")
                self.to_date = date.strftime("%Y-%m-%d")
            date = (datetime.now() - relativedelta(days=7))
            if self.date_range == 'last_week':
                day_today = date - timedelta(days=date.weekday())
                self.from_date = (day_today - timedelta(days=date.weekday())).strftime("%Y-%m-%d")
                self.to_date = (day_today + timedelta(days=6)).strftime("%Y-%m-%d")
            date = (datetime.now() - relativedelta(months=1))
            if self.date_range == 'last_month':
                self.from_date = datetime(date.year, date.month, 1).strftime("%Y-%m-%d")
                self.to_date = datetime(date.year, date.month, calendar.mdays[date.month]).strftime("%Y-%m-%d")
            date = (datetime.now() - relativedelta(months=3))
            if self.date_range == 'last_quarter':
                if int((date.month - 1) / 3) == 0:  # First quarter
                    self.from_date = datetime(date.year, 1, 1).strftime("%Y-%m-%d")
                    self.to_date = datetime(date.year, 3, calendar.mdays[3]).strftime("%Y-%m-%d")
                if int((date.month - 1) / 3) == 1:  # Second quarter
                    self.from_date = datetime(date.year, 4, 1).strftime("%Y-%m-%d")
                    self.to_date = datetime(date.year, 6, calendar.mdays[6]).strftime("%Y-%m-%d")
                if int((date.month - 1) / 3) == 2:  # Third quarter
                    self.from_date = datetime(date.year, 7, 1).strftime("%Y-%m-%d")
                    self.to_date = datetime(date.year, 9, calendar.mdays[9]).strftime("%Y-%m-%d")
                if int((date.month - 1) / 3) == 3:  # Fourth quarter
                    self.from_date = datetime(date.year, 10, 1).strftime("%Y-%m-%d")
                    self.to_date = datetime(date.year, 12, calendar.mdays[12]).strftime("%Y-%m-%d")
            date = (datetime.now() - relativedelta(years=1))
            if self.date_range == 'last_financial_year':
                    self.from_date = datetime(date.year, 1, 1).strftime("%Y-%m-%d")
                    self.to_date = datetime(date.year, 12, 31).strftime("%Y-%m-%d")
    def open_view(self):
        print("open_view")
        fm_date='YYYY-MM-DD'
        t_date='YYYY-MM-DD'
        if self.from_date :
            fm_date=self.from_date.strftime("%Y-%m-%d")
        if self.to_date:
            t_date= self.to_date.strftime("%Y-%m-%d") 
        data={
             'partner_id': self.partner_id.id,
            #  'journal_id':self.journal_id.id,
             'salesman_id':self.salesman_id.id,
            #  'product_id':self.product_id.ids,
            #  'product_type': self.product_type,
            #  'pro_cate_id': self.pro_cate_id.id,
            'from_date':fm_date  ,
            'to_date': t_date,
            'type_payment':self.type_payment,
            'analysis_account_id': self.analysis_account_id.id,
            'company_ids': self.company_ids.ids,
            # 'show_payment_this_company': self.show_payment_this_company,
            # 'order_view':self.order_view,
            # 'choose_order_company_view':self.choose_order_company_view,
            'user_id':self.user_id.id,
            # 'state':self.state,
             'hide_payment_cancel':self.hide_payment_cancel,
        }
        print(data,"dataaaaaaaaa1")
        json_file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data.json')
        with open(json_file_path, 'w') as json_file:
            json_file.write('[]')

        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file)
        
        result={
            'type': 'ir.actions.client',
            'tag': 'yousentech_sale_reports.paytoday_re',
        }
        return result
   
    @api.model
    def process_data_report_payment(self):
        json_file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data.json')
        jour_id_data=[]
        data = []
        if not os.path.exists(json_file_path):
            with open(json_file_path, 'w') as json_file:
                json_file.write('[]')
                # print(data,"dataaa2")
                return data   
        else:
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)
                with open(json_file_path, 'w') as json_file:
                    json_file.write('[]')
                    # print("clear2")
                # print("read")
                # print(data,"dataaa3")
                return data  
    @api.model 
    def get_report_payment(self, *args, **kwargs):
        print("get_report_paymenttoday")
        data=[]
        jour_id_data=[]
        company=[]
       
        show=False
        show_name_analysis=''
        show_name_categ=''
        for arg in args:
            sum_amount_untaxed=0
            sum_amount_with_tax=0
            sum_amount_bank=0
            sum_amount_tax=0
            sum_amount_cash=0
            sum_quantity=0 
            sum_amount_radiuse=0  
            if arg:
                domain_analysis=[]
                analysis_data=[]
                print(arg)
                domain=[]
                domain_acc_move=[]
                move_line = [] 
                companies = []
                
                if arg['partner_id'] and arg['partner_id']!=0 :
                    domain.append(('partner_id','in',[arg['partner_id']]))
                    domain_analysis.append(('partner_id','in',[arg['partner_id']]))
                # if arg['journal_id'] and arg['journal_id']!=0:
                #     domain.append(('journal_id','in',[arg['journal_id']]))
                #     domain_analysis.append(('journal_id','in',[arg['journal_id']]))
                if arg['salesman_id'] and arg['salesman_id']!=0:
                    domain.append(('salesman_id','in',[arg['salesman_id']]))
                
                if arg['from_date']!='YYYY-MM-DD'  and arg['to_date']!='YYYY-MM-DD':
                    domain.append(('date', '>=',arg['from_date']))
                    domain.append(('date', '<=',arg['to_date']))
                    domain_analysis.append(('date', '>=',arg['from_date']))
                    domain_analysis.append(('date', '<=',arg['to_date']))
                   
                  
                user_id_now=self.env.user 
                # if arg['show_payment_this_company']:
                    
                if arg['company_ids'] :
                    companies=self.env['res.company'].search([('id','in',arg['company_ids'])])
                else :
                    companies=self.env['res.company'].search([('id','in',user_id_now.company_ids.ids)])
                # else :
                #     companies=self.env['res.company'].search([('id','in',user_id_now.company_ids.ids)])    
                
                domain.append(('company_id','in',companies.ids))
                domain_analysis.append(('company_id','in',companies.ids))
                for com in companies:
                    company.append(com.name)
                if arg['hide_payment_cancel']==True:
                    domain.append(('state','!=','draft'))
                if arg['type_payment']=='out_refund' :
                    domain.append(('move_type','=','out_refund'))
                elif arg['type_payment']=='out_invoice' :
                    domain.append(('move_type','=','out_invoice'))
                else:
                    domain.append('|')
                    domain.append(('move_type','=','out_invoice'))
                    domain.append(('move_type','=','out_refund'))      
                move_line=self.env['account.move'].search(
                domain,
                )
                payments= self.env['account.payment'].search(
                    ['|',('journal_id.type','=','bank'),('journal_id.type','=','cash')]
                )
                move_line.sorted('name')
                jouranls=self.env['account.payment.method.line'].search(
                ['|',('journal_id.type','=','bank') ,('journal_id.type','=','cash')]
                ).journal_id.ids
                print(jouranls,'jouranls')
                for jor_id in jouranls:
                    sum_amo_jou=0
                    journal_details=self.env['account.journal'].search(
                     [('id','in',[jor_id])]
                    )
                    if journal_details:
                        for recode in move_line:
                            domain_move_line_analysis=[]
                            domain_move_line_analysis.append(('move_id','in',[recode.id]))
                            if arg['analysis_account_id'] and arg['analysis_account_id']!=0:
                                analysis_account=self.env['account.analytic.line'].search(
                                ['|',('account_id','in',[arg['analysis_account_id']]),('x_plan2_id','in',[arg['analysis_account_id']])]
                                )

                                domain_analysis.append(('id','in',analysis_account.ids))

                                analysis_data=self.env['account.analytic.line'].search(
                                    domain_analysis,  
                                    )
                                print(analysis_data,'analysis_dataanalysis_data')
                                domain_move_line_analysis.append(('id','in',analysis_data.move_line_id.ids))
                            move_line_details_analysis=self.env['account.move.line'].search(
                                domain_move_line_analysis
                            )  
                           
                            if move_line_details_analysis:
                                amount_jou=sum(item.amount for item in payments.filtered(lambda x:x.journal_id.id==journal_details.id and x.reconciled_invoice_ids.id==recode.id))
                                sum_amo_jou+=amount_jou
                                
                        jo_line={
                            'id':journal_details.id,
                            'name':journal_details.name,
                            'total':round(sum_amo_jou, 2)
                        }
                        jour_id_data.append(jo_line) 
                
                
                
                # payment_receivable
                for recode in move_line:
                    domain_move_line_analysis=[]
                    domain_move_line_analysis.append(('move_id','in',[recode.id]))
                    if arg['analysis_account_id'] and arg['analysis_account_id']!=0:
                        analysis_account=self.env['account.analytic.line'].search(
                        ['|',('account_id','in',[arg['analysis_account_id']]),('x_plan2_id','in',[arg['analysis_account_id']])]
                        )

                        domain_analysis.append(('id','in',analysis_account.ids))

                        analysis_data=self.env['account.analytic.line'].search(
                            domain_analysis,  
                            )
                        print(analysis_data,'analysis_dataanalysis_data')
                        domain_move_line_analysis.append(('id','in',analysis_data.move_line_id.ids))
                    move_line_details_analysis=self.env['account.move.line'].search(
                        domain_move_line_analysis
                    )    
                    # payments= self.env['account.payment'].search(
                    #     ['|',('journal_id.type','=','bank'),('journal_id.type','=','cash')]
                    # )
                    if move_line_details_analysis:
                        amou_bank=sum(item.amount for item in payments.filtered(lambda x:x.journal_id.type=='bank' and x.reconciled_invoice_ids.id==recode.id))
                        amount_cash=sum(item.amount for item in payments.filtered(lambda x:x.journal_id.type=='cash' and x.reconciled_invoice_ids.id==recode.id))
                        amou_with_tax=sum(item.price_total for item in recode.invoice_line_ids.filtered(lambda x:x.price_total>=x.price_subtotal))
                        amount_untaxed=recode.amount_untaxed
                        amount_tax=recode.amount_tax
                        amount_radiuse=amou_with_tax -(amount_cash+amou_bank)

                        sum_amount_untaxed+=amount_untaxed
                        sum_amount_with_tax+=amou_with_tax
                        sum_amount_bank+=amou_bank
                        sum_amount_tax+=amount_tax
                        sum_amount_cash+=amount_cash
                        sum_amount_radiuse+=amount_radiuse
                        # sum_quantity+=sum_qut
                        
                        
                        
                                    
                        line={
                            'id':recode.id,
                            'id_l':recode.id,
                            'prodect_name':'',
                            'name':recode.name,
                            'date':recode.date,
                            'move_type':"Sale Invoice" if recode.move_type=='out_invoice' else "Refund",
                            'partner_name':recode.partner_id.name,
                            'amount_untaxed': round(amount_untaxed, 2),
                            'amount_tax':round(amount_tax, 2) ,
                            'amount_with_tax':round(amou_with_tax, 2),
                            'amount_bank':round(amou_bank, 2),
                            'amount_cash':round(amount_cash, 2),
                            'amount_radiuse':round(amount_radiuse, 2),
                            'quantity': 0,
                            
                            
                            }
                        data.append(line) 
                 

        
        line_data={
            'data':data,
            'jour_id_data':jour_id_data,
            'company':company,
            'show_product':show,
            'show_name_analysis':show_name_analysis,
            'show_name_categ':show_name_categ,
            'sum_amount_untaxed':round(sum_amount_untaxed,2) ,
            'sum_amount_with_tax':round(sum_amount_with_tax,2) ,
            'sum_amount_bank':round(sum_amount_bank,2) ,
            'sum_amount_tax':round(sum_amount_tax,2) ,
            'sum_amount_cash':round(sum_amount_cash,2) ,
            'sum_amount_radiuse':round(sum_amount_radiuse,2) ,
            'sum_quantity': round(sum_quantity ,2) ,
       
        }
        print(data)
        return line_data
    
    

    @api.model 
    def get_accounts_report(self):
        data=[]
        partner = self.env['res.partner'].search([])
        partner_list=[]
        saleman_list=[]
        analysis_account_list=[]
        journal_ids_list=[]
        line_defualt={
                'id':0,
                'name':'',
                   
            }
        partner_list.append(line_defualt)
        
        line_defualt2={
                'id':0,
                'name':'',
            }
        saleman_list.append(line_defualt2)
        journal_ids_list.append((line_defualt2))
        analysis_account_list.append(line_defualt2)

        for recode in partner:
            line={
                'id':recode['id'],
                'name':recode['name'],
            }
            partner_list.append(line)
        analysis_account = self.env['account.analytic.account'].search([])
        for recode in analysis_account:
            line={
                'id':recode['id'],
                'name':recode['name'],
            }
            analysis_account_list.append(line)
        saleman = self.env['salesman'].search([])
        for recode in saleman:
            line={
                'id':recode['id'],
                'name':recode['name'],
            }
            saleman_list.append(line)
        journal_ids = self.env['account.journal'].search([])
        for recode in journal_ids:
            line={
                'id':recode['id'],
                'name':recode['code']+' '+recode['name'],
            }
            journal_ids_list.append(line)
        lines={
            'partner_list':partner_list,
            'saleman_list':saleman_list,
            'analysis_account_list':analysis_account_list,
            'journal_ids_list':journal_ids_list 
        }
        data.append(lines)
        return data       

    def get_pdf_report(self):
        """Call when button 'Get Report' clicked.
            """
        print("get_pdf_report")
        fm_date='YYYY-MM-DD'
        t_date='YYYY-MM-DD'
        if self.from_date :
            fm_date=self.from_date.strftime("%Y-%m-%d")
        if self.to_date:
            t_date= self.to_date.strftime("%Y-%m-%d") 
        data={
             'partner_id': self.partner_id.id,
             'partner_name': self.partner_id.name,
            #  'journal_id':self.journal_id.id,
             'salesman_id':self.salesman_id.id,
             'salesman_name':self.salesman_id.name,
            #  'product_id':self.product_id.ids,
            #  'product_type': self.product_type,
            #  'pro_cate_id': self.pro_cate_id.id,
            'from_date':fm_date  ,
            'to_date': t_date,
            'type_payment':self.type_payment,
            'analysis_account_id': self.analysis_account_id.id,
            'analysis_account_name': self.analysis_account_id.name,
            'company_ids': self.company_ids.ids,
            # 'show_payment_this_company': self.show_payment_this_company,
            # 'order_view':self.order_view,
            # 'choose_order_company_view':self.choose_order_company_view,
            'user_id':self.user_id.id,
            # 'state':self.state,
             'hide_payment_cancel':self.hide_payment_cancel,
        }
        print(data,"dataaaaaaaaa1")
        

        return self.env.ref('yousentech_sale_reports.print_daily_sale_rpt').report_action(self, data=data)

    def get_excel_report(self):
        
        fm_date='YYYY-MM-DD'
        t_date='YYYY-MM-DD'
        if self.from_date :
            fm_date=self.from_date.strftime("%Y-%m-%d")
        if self.to_date:
            t_date= self.to_date.strftime("%Y-%m-%d") 
        data={
             'partner_id': self.partner_id.id,
             'partner_name': self.partner_id.name,
            #  'journal_id':self.journal_id.id,
             'salesman_id':self.salesman_id.id,
             'salesman_name':self.salesman_id.name,
            #  'product_id':self.product_id.ids,
            #  'product_type': self.product_type,
            #  'pro_cate_id': self.pro_cate_id.id,
            'from_date':fm_date  ,
            'to_date': t_date,
            'type_payment':self.type_payment,
            'analysis_account_id': self.analysis_account_id.id,
            'analysis_account_name': self.analysis_account_id.name,
            'company_ids': self.company_ids.ids,
            'company_name': self.company_ids.name,
            # 'show_payment_this_company': self.show_payment_this_company,
            # 'order_view':self.order_view,
            # 'choose_order_company_view':self.choose_order_company_view,
            'user_id':self.user_id.id,
            # 'state':self.state,
             'hide_payment_cancel':self.hide_payment_cancel,
        }
        print(data,"dataaaaaaaaa1")
        # name = self.env['account.move'].search(data)
        return self.env.ref('yousentech_sale_reports.excl_daily_sale_rpt').report_action(self,data)  
class daily_saleXlsx(models.AbstractModel):
    _name = 'report.yousentech_sale_reports.report_xlsx_daily_sale'
    _inherit = "report.report_xlsx.abstract"
    def generate_xlsx_report(self, workbook, data, patients):
        datas=[]
        jour_id_data=[]
        company=[]
       
        show=False
        show_name_analysis=''
        show_name_categ=''
        sum_amount_untaxed=0
        sum_amount_with_tax=0
        sum_amount_bank=0
        sum_amount_tax=0
        sum_amount_cash=0
        sum_quantity=0 
        sum_amount_radiuse=0  
        arg =data  
        if arg:
                domain_analysis=[]
                analysis_data=[]
                print(arg)
                domain=[]
                domain_acc_move=[]
                move_line = [] 
                companies = []
                
                if arg['partner_id'] and arg['partner_id']!=0 :
                    domain.append(('partner_id','in',[arg['partner_id']]))
                    domain_analysis.append(('partner_id','in',[arg['partner_id']]))
                # if arg['journal_id'] and arg['journal_id']!=0:
                #     domain.append(('journal_id','in',[arg['journal_id']]))
                #     domain_analysis.append(('journal_id','in',[arg['journal_id']]))
                if arg['salesman_id'] and arg['salesman_id']!=0:
                    domain.append(('salesman_id','in',[arg['salesman_id']]))
                
                if arg['from_date']!='YYYY-MM-DD'  and arg['to_date']!='YYYY-MM-DD':
                    domain.append(('date', '>=',arg['from_date']))
                    domain.append(('date', '<=',arg['to_date']))
                    domain_analysis.append(('date', '>=',arg['from_date']))
                    domain_analysis.append(('date', '<=',arg['to_date']))
                   
                  
                user_id_now=self.env.user 
                # if arg['show_payment_this_company']:
                    
                if arg['company_ids'] :
                    companies=self.env['res.company'].search([('id','in',arg['company_ids'])])
                else :
                    companies=self.env['res.company'].search([('id','in',user_id_now.company_ids.ids)])
                # else :
                #     companies=self.env['res.company'].search([('id','in',user_id_now.company_ids.ids)])    
                
                domain.append(('company_id','in',companies.ids))
                domain_analysis.append(('company_id','in',companies.ids))
                for com in companies:
                    company.append(com.name)
                if arg['hide_payment_cancel']==True:
                    domain.append(('state','!=','draft'))
                if arg['type_payment']=='out_refund' :
                    domain.append(('move_type','=','out_refund'))
                elif arg['type_payment']=='out_invoice' :
                    domain.append(('move_type','=','out_invoice'))
                else:
                    domain.append('|')
                    domain.append(('move_type','=','out_invoice'))
                    domain.append(('move_type','=','out_refund'))      
                move_line=self.env['account.move'].search(
                domain,
                )
                payments= self.env['account.payment'].search(
                    ['|',('journal_id.type','=','bank'),('journal_id.type','=','cash')]
                )
                move_line.sorted('name')
                jouranls=self.env['account.payment.method.line'].search(
                ['|',('journal_id.type','=','bank') ,('journal_id.type','=','cash')]
                ).journal_id.ids
                print(jouranls,'jouranls')
                for jor_id in jouranls:
                    sum_amo_jou=0
                    journal_details=self.env['account.journal'].search(
                     [('id','in',[jor_id])]
                    )
                    if journal_details:
                        for recode in move_line:
                            domain_move_line_analysis=[]
                            domain_move_line_analysis.append(('move_id','in',[recode.id]))
                            if arg['analysis_account_id'] and arg['analysis_account_id']!=0:
                                analysis_account=self.env['account.analytic.line'].search(
                                ['|',('account_id','in',[arg['analysis_account_id']]),('x_plan2_id','in',[arg['analysis_account_id']])]
                                )

                                domain_analysis.append(('id','in',analysis_account.ids))

                                analysis_data=self.env['account.analytic.line'].search(
                                    domain_analysis,  
                                    )
                                print(analysis_data,'analysis_dataanalysis_data')
                                domain_move_line_analysis.append(('id','in',analysis_data.move_line_id.ids))
                            move_line_details_analysis=self.env['account.move.line'].search(
                                domain_move_line_analysis
                            )  
                           
                            if move_line_details_analysis:
                                amount_jou=sum(item.amount for item in payments.filtered(lambda x:x.journal_id.id==journal_details.id and x.reconciled_invoice_ids.id==recode.id))
                                sum_amo_jou+=amount_jou
                                
                        jo_line={
                            'id':journal_details.id,
                            'name':journal_details.name,
                            'total':round(sum_amo_jou, 2)
                        }
                        jour_id_data.append(jo_line) 
 
                # payment_receivable
                for recode in move_line:
                    domain_move_line_analysis=[]
                    domain_move_line_analysis.append(('move_id','in',[recode.id]))
                    if arg['analysis_account_id'] and arg['analysis_account_id']!=0:
                        analysis_account=self.env['account.analytic.line'].search(
                        ['|',('account_id','in',[arg['analysis_account_id']]),('x_plan2_id','in',[arg['analysis_account_id']])]
                        )

                        domain_analysis.append(('id','in',analysis_account.ids))

                        analysis_data=self.env['account.analytic.line'].search(
                            domain_analysis,  
                            )
                        print(analysis_data,'analysis_dataanalysis_data')
                        domain_move_line_analysis.append(('id','in',analysis_data.move_line_id.ids))
                    move_line_details_analysis=self.env['account.move.line'].search(
                        domain_move_line_analysis
                    )    
                    # payments= self.env['account.payment'].search(
                    #     ['|',('journal_id.type','=','bank'),('journal_id.type','=','cash')]
                    # )
                    if move_line_details_analysis:
                        amou_bank=sum(item.amount for item in payments.filtered(lambda x:x.journal_id.type=='bank' and x.reconciled_invoice_ids.id==recode.id))
                        amount_cash=sum(item.amount for item in payments.filtered(lambda x:x.journal_id.type=='cash' and x.reconciled_invoice_ids.id==recode.id))
                        amou_with_tax=sum(item.price_total for item in recode.invoice_line_ids.filtered(lambda x:x.price_total>=x.price_subtotal))
                        amount_untaxed=recode.amount_untaxed
                        amount_tax=recode.amount_tax
                        amount_radiuse=amou_with_tax -(amount_cash+amou_bank)

                        sum_amount_untaxed+=amount_untaxed
                        sum_amount_with_tax+=amou_with_tax
                        sum_amount_bank+=amou_bank
                        sum_amount_tax+=amount_tax
                        sum_amount_cash+=amount_cash
                        sum_amount_radiuse+=amount_radiuse
                        # sum_quantity+=sum_qut
                                
                        line={
                            'id':recode.id,
                            'id_l':recode.id,
                            'prodect_name':'',
                            'name':recode.name,
                            'date':recode.date,
                            'move_type':"فاتورة مبيعات" if recode.move_type=='out_invoice' else "فاتورة مرتجع",
                            'partner_name':recode.partner_id.name,
                            'amount_untaxed': round(amount_untaxed, 2),
                            'amount_tax':round(amount_tax, 2) ,
                            'amount_with_tax':round(amou_with_tax, 2),
                            'amount_bank':round(amou_bank, 2),
                            'amount_cash':round(amount_cash, 2),
                            'amount_radiuse':round(amount_radiuse, 2),
                            'quantity': 0,
                            
                            
                            }
                        datas.append(line) 
        docs=[{
            'data':data,
            'datas':datas,
            'jour_id_data':jour_id_data,
            'company':company,
            'show_product':show,
            'show_name_analysis':show_name_analysis,
            'show_name_categ':show_name_categ,
            'sum_amount_untaxed':round(sum_amount_untaxed,2) ,
            'sum_amount_with_tax':round(sum_amount_with_tax,2) ,
            'sum_amount_bank':round(sum_amount_bank,2) ,
            'sum_amount_tax':round(sum_amount_tax,2) ,
            'sum_amount_cash':round(sum_amount_cash,2) ,
            'sum_amount_radiuse':round(sum_amount_radiuse,2) ,
            'sum_quantity': round(sum_quantity ,2) ,
       
        }]
        
        print('docs',docs)
        
        format_header = workbook.add_format(
                        {'bold': True, 'align': 'center', 'font': 'Times New Roman', 'font_size': 16,'bg_color': '#C5C3C3',})
        format_header.set_bg_color('#fffbed')
        format_date = workbook.add_format(
                        {'num_format': 'dd-mm-yyyy', 'align': 'center', 'font': 'Times New Roman', 'font_size': 11})
        format_num = workbook.add_format(
                        {"num_format": u"#,##0.00", 'align': 'center', 'font': 'Times New Roman', 'font_size': 11})
        format_string = workbook.add_format(
                        {'align': 'center', 'font': 'Times New Roman', 'font_size': 10})
        format_string.set_border(3)
        format_num.set_border(3)
        format_date.set_border(3)
        format_top = workbook.add_format(
                        {'bg_color': '#fffbed','bold': True,'align': 'center', 'font': 'Times New Roman', 'font_size': 11 ,"num_format": u"#,##0.00",})
        format_top.set_border(5)
        sheet = workbook.add_worksheet('Daily Sale Report')
        if self.env.user.lang in ['ar_001','ar_SY']:
                sheet.right_to_left()
        header_row_style = workbook.add_format({'bold': True,'font': 'Times New Roman', 'align': 'center', 'border': True, "bg_color": "#e9967a"})
              
        header_row=1
        header_col=2
        # row = 3
        # col = 1
        sheet.merge_range(header_row, header_col, header_row, header_col + 5,'Daily Sale Report',   format_header)
        info_style = workbook.add_format(
            {
                "font_size": 13,
                "font": "Times New Roman",
                "bold": True,
                "align": "center",
            }
        )
        info_row = 3
        info_row2 = 3
        info_col = 2
       
        sheet.write(info_row, info_col, "From Date ", info_style)
        if docs[0]["data"]["from_date"] != "YYYY-MM-DD":
            sheet.write(
                info_row, info_col + 1, docs[0]["data"]["from_date"], info_style
            )
        info_row+=1
            
        sheet.write(info_row, info_col , "To Date ", info_style)
        if docs[0]["data"]["to_date"] != "YYYY-MM-DD":
            sheet.write(info_row, info_col + 1, docs[0]["data"]["to_date"], info_style)
        info_row+=1
        if docs[0]["data"]["type_payment"] :
            sheet.write(info_row, info_col , "Report Type ", info_style)
            sheet.write(info_row, info_col + 1, docs[0]["data"]["type_payment"], info_style)
        info_row+=1
        if docs[0]["data"]["analysis_account_name"]:
            sheet.write(info_row2, info_col+2, "Analysis Account", info_style)
            sheet.merge_range(
                info_row2,
                info_col +3,
                info_row2,
                info_col + 4,
                docs[0]["data"]["analysis_account_name"],
                info_style,
            )
            info_row2 += 1
            
        if docs[0]["data"]["partner_name"]:
            sheet.write(info_row2, info_col+2, "Partner Name", info_style)
            sheet.merge_range(
                info_row2,
                info_col +3,
                info_row2,
                info_col + 4,
                docs[0]["data"]["partner_name"],
                info_style,
            )
            info_row2 += 1
        if docs[0]["data"]["salesman_name"]:
            sheet.write(info_row2, info_col+2, "Salesman Name", info_style)
            sheet.merge_range(
                info_row2,
                info_col +3,
                info_row2,
                info_col + 4,
                docs[0]["data"]["salesman_name"],
                info_style,
            )
            info_row2 += 1
        if docs[0]["data"]["company_name"]:
            sheet.write(info_row2, info_col+2, "company", info_style)
            sheet.merge_range(
                info_row2,
                info_col +3,
                info_row2,
                info_col + 4,
                docs[0]["data"]["company_name"],
                info_style,
            )
            info_row2 += 1


        # if docs[0]["data"]['show_pruchase_this_company']:
        #     sheet.write(info_row2, info_col+2, "Company:", info_style)
        #     print('com',docs[0]["data"]['companies'])
        #     #  '\n'.join
        #     if docs[0]["data"]['companies']:
        #       for index,com in enumerate( docs[0]["data"]['companies']):
        #         sheet.write(info_row2, info_col + 3,(com['name'])+' ',info_style)
        #         info_col+=1
        #       info_row2 +=1
        #     else:
        #         sheet.write(info_row2, info_col+2, "Company:", info_style)
        #         sheet.write(info_row2, info_col + 3, "All", info_style)
        #         info_row2 +=1
        # else :
        #     sheet.write(info_row2, info_col+2, "Company:", info_style)
        #     sheet.write(info_row2, info_col + 3, "All", info_style)
        #     info_row2 +=1

        row = info_row2 + 2
        col = 1
        for obj in docs :
            sheet.set_column(0, 0, 8)
            sheet.set_column(1, 10, 18)
            sheet.write(row, col, 'Date', header_row_style)
            sheet.write(row, col+1, 'Invoice Type', header_row_style)
            sheet.write(row, col+2,  'Inv NO', header_row_style)
            sheet.write(row, col+3,  'Partner', header_row_style)

            sheet.write(row, col+4, 'Basic Total', header_row_style)
            sheet.write(row, col+5, 'Total taxs', header_row_style)
            sheet.write(row, col+6,  'Total including taxs', header_row_style)
            sheet.write(row, col+7, 'Paid in cash', header_row_style)
            sheet.write(row, col+8, 'Paid in bank', header_row_style)
            sheet.write(row, col+9, 'Residual', header_row_style)
            if obj["show_product"]:
               sheet.write(row, col+10, '-', format_top)
               sheet.write(row, col+11, 'quantity', format_top)
        # row += 2
        row += 1
        
        sheet.write(row, col, 'Total', format_top)
        sheet.write(row, col+1, '-', format_top)
        sheet.write(row, col+2,  '-', format_top)
        sheet.write(row, col+3, '-', format_top)
        sheet.write(row, col+4, obj['sum_amount_untaxed'], format_top)
        sheet.write(row, col+5, obj['sum_amount_tax'], format_top)
        sheet.write(row, col+6, obj['sum_amount_with_tax'], format_top)
        sheet.write(row, col+7, obj['sum_amount_cash'], format_top)
        
        sheet.write(row, col+8,obj['sum_amount_bank'] ,format_top)
        sheet.write(row, col+9, obj['sum_amount_radiuse'], format_top)
        if obj["show_product"]:
            sheet.write(row, col+10,'-' ,format_top)
            sheet.write(row, col+11, obj['sum_quantity'], format_top)
        row += 1
        for item in obj['datas'] :   
            sheet.write(row, col, item['date'], format_date )
            sheet.write(row, col+1, item['move_type'], format_string)
            sheet.write(row, col+2, item['name'], format_string)
            sheet.write(row, col+3, item['partner_name'], format_num)
            sheet.write(row, col+4,  item['amount_untaxed'], format_num)
            sheet.write(row, col+5,  item['amount_tax'], format_num)
            sheet.write(row, col+6,  item['amount_with_tax'], format_num)
            sheet.write(row, col+7,  item['amount_cash'], format_num)
            sheet.write(row, col+8, item['amount_bank'], format_string)
            sheet.write(row, col+9, item['amount_radiuse'], format_num)
            if obj["show_product"]:
                sheet.write(row, col+10, item['prodect_name'], format_string)
                sheet.write(row, col+11, item['quantity'], format_num)
            row += 1
            
            

class dailysalespdfReport(models.AbstractModel):
    _name = 'report.yousentech_sale_reports.pdf_daily_sale_temp'
        
    @api.model
    def _get_report_values(self, *args, data=None):
        print("get_report_daily_sale")
        datas=[]
        jour_id_data=[]
        company=[]
       
        show=False
        show_name_analysis=''
        show_name_categ=''
        sum_amount_untaxed=0
        sum_amount_with_tax=0
        sum_amount_bank=0
        sum_amount_tax=0
        sum_amount_cash=0
        sum_quantity=0 
        sum_amount_radiuse=0  
        arg =data  
        if arg:
                domain_analysis=[]
                analysis_data=[]
                print(arg)
                domain=[]
                domain_acc_move=[]
                move_line = [] 
                companies = []
                
                if arg['partner_id'] and arg['partner_id']!=0 :
                    domain.append(('partner_id','in',[arg['partner_id']]))
                    domain_analysis.append(('partner_id','in',[arg['partner_id']]))
                # if arg['journal_id'] and arg['journal_id']!=0:
                #     domain.append(('journal_id','in',[arg['journal_id']]))
                #     domain_analysis.append(('journal_id','in',[arg['journal_id']]))
                if arg['salesman_id'] and arg['salesman_id']!=0:
                    domain.append(('salesman_id','in',[arg['salesman_id']]))
                
                if arg['from_date']!='YYYY-MM-DD'  and arg['to_date']!='YYYY-MM-DD':
                    domain.append(('date', '>=',arg['from_date']))
                    domain.append(('date', '<=',arg['to_date']))
                    domain_analysis.append(('date', '>=',arg['from_date']))
                    domain_analysis.append(('date', '<=',arg['to_date']))
                   
                  
                user_id_now=self.env.user 
                # if arg['show_payment_this_company']:
                    
                if arg['company_ids'] :
                    companies=self.env['res.company'].search([('id','in',arg['company_ids'])])
                else :
                    companies=self.env['res.company'].search([('id','in',user_id_now.company_ids.ids)])
                # else :
                #     companies=self.env['res.company'].search([('id','in',user_id_now.company_ids.ids)])    
                
                domain.append(('company_id','in',companies.ids))
                domain_analysis.append(('company_id','in',companies.ids))
                for com in companies:
                    company.append(com.name)
                if arg['hide_payment_cancel']==True:
                    domain.append(('state','!=','draft'))
                if arg['type_payment']=='out_refund' :
                    domain.append(('move_type','=','out_refund'))
                elif arg['type_payment']=='out_invoice' :
                    domain.append(('move_type','=','out_invoice'))
                else:
                    domain.append('|')
                    domain.append(('move_type','=','out_invoice'))
                    domain.append(('move_type','=','out_refund'))      
                move_line=self.env['account.move'].search(
                domain,
                )
                payments= self.env['account.payment'].search(
                    ['|',('journal_id.type','=','bank'),('journal_id.type','=','cash')]
                )
                move_line.sorted('name')
                jouranls=self.env['account.payment.method.line'].search(
                ['|',('journal_id.type','=','bank') ,('journal_id.type','=','cash')]
                ).journal_id.ids
                print(jouranls,'jouranls')
                for jor_id in jouranls:
                    sum_amo_jou=0
                    journal_details=self.env['account.journal'].search(
                     [('id','in',[jor_id])]
                    )
                    if journal_details:
                        for recode in move_line:
                            domain_move_line_analysis=[]
                            domain_move_line_analysis.append(('move_id','in',[recode.id]))
                            if arg['analysis_account_id'] and arg['analysis_account_id']!=0:
                                analysis_account=self.env['account.analytic.line'].search(
                                ['|',('account_id','in',[arg['analysis_account_id']]),('x_plan2_id','in',[arg['analysis_account_id']])]
                                )

                                domain_analysis.append(('id','in',analysis_account.ids))

                                analysis_data=self.env['account.analytic.line'].search(
                                    domain_analysis,  
                                    )
                                print(analysis_data,'analysis_dataanalysis_data')
                                domain_move_line_analysis.append(('id','in',analysis_data.move_line_id.ids))
                            move_line_details_analysis=self.env['account.move.line'].search(
                                domain_move_line_analysis
                            )  
                           
                            if move_line_details_analysis:
                                amount_jou=sum(item.amount for item in payments.filtered(lambda x:x.journal_id.id==journal_details.id and x.reconciled_invoice_ids.id==recode.id))
                                sum_amo_jou+=amount_jou
                                
                        jo_line={
                            'id':journal_details.id,
                            'name':journal_details.name,
                            'total':round(sum_amo_jou, 2)
                        }
                        jour_id_data.append(jo_line) 
 
                # payment_receivable
                for recode in move_line:
                    domain_move_line_analysis=[]
                    domain_move_line_analysis.append(('move_id','in',[recode.id]))
                    if arg['analysis_account_id'] and arg['analysis_account_id']!=0:
                        analysis_account=self.env['account.analytic.line'].search(
                        ['|',('account_id','in',[arg['analysis_account_id']]),('x_plan2_id','in',[arg['analysis_account_id']])]
                        )

                        domain_analysis.append(('id','in',analysis_account.ids))

                        analysis_data=self.env['account.analytic.line'].search(
                            domain_analysis,  
                            )
                        print(analysis_data,'analysis_dataanalysis_data')
                        domain_move_line_analysis.append(('id','in',analysis_data.move_line_id.ids))
                    move_line_details_analysis=self.env['account.move.line'].search(
                        domain_move_line_analysis
                    )    
                    # payments= self.env['account.payment'].search(
                    #     ['|',('journal_id.type','=','bank'),('journal_id.type','=','cash')]
                    # )
                    if move_line_details_analysis:
                        amou_bank=sum(item.amount for item in payments.filtered(lambda x:x.journal_id.type=='bank' and x.reconciled_invoice_ids.id==recode.id))
                        amount_cash=sum(item.amount for item in payments.filtered(lambda x:x.journal_id.type=='cash' and x.reconciled_invoice_ids.id==recode.id))
                        amou_with_tax=sum(item.price_total for item in recode.invoice_line_ids.filtered(lambda x:x.price_total>=x.price_subtotal))
                        amount_untaxed=recode.amount_untaxed
                        amount_tax=recode.amount_tax
                        amount_radiuse=amou_with_tax -(amount_cash+amou_bank)

                        sum_amount_untaxed+=amount_untaxed
                        sum_amount_with_tax+=amou_with_tax
                        sum_amount_bank+=amou_bank
                        sum_amount_tax+=amount_tax
                        sum_amount_cash+=amount_cash
                        sum_amount_radiuse+=amount_radiuse
                        # sum_quantity+=sum_qut
                                
                        line={
                            'id':recode.id,
                            'id_l':recode.id,
                            'prodect_name':'',
                            'name':recode.name,
                            'date':recode.date,
                            'move_type':"فاتورة مبيعات" if recode.move_type=='out_invoice' else "فاتورة مرتجع",
                            'partner_name':recode.partner_id.name,
                            'amount_untaxed': round(amount_untaxed, 2),
                            'amount_tax':round(amount_tax, 2) ,
                            'amount_with_tax':round(amou_with_tax, 2),
                            'amount_bank':round(amou_bank, 2),
                            'amount_cash':round(amount_cash, 2),
                            'amount_radiuse':round(amount_radiuse, 2),
                            'quantity': 0,
                            
                            
                            }
                        datas.append(line) 
        return{
            'data':data,
            'datas':datas,
            'jour_id_data':jour_id_data,
            'mycompany':company,
            'current_company':self.env.company,
            "current_lang" : self.env.user.lang,
            'show_product':show,
            'show_name_analysis':show_name_analysis,
            'show_name_categ':show_name_categ,
            'sum_amount_untaxed':round(sum_amount_untaxed,2) ,
            'sum_amount_with_tax':round(sum_amount_with_tax,2) ,
            'sum_amount_bank':round(sum_amount_bank,2) ,
            'sum_amount_tax':round(sum_amount_tax,2) ,
            'sum_amount_cash':round(sum_amount_cash,2) ,
            'sum_amount_radiuse':round(sum_amount_radiuse,2) ,
            'sum_quantity': round(sum_quantity ,2) ,
       
        }
        