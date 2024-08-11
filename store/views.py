from django.shortcuts import render,redirect

from store.forms import SignupForm,SigninForm

from django.views.generic import View

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from store.models import Product,Basket,BasketItem,Size,Order








# Create your views here.

class RegistrationView(View):
    
    def get(self,request,*args, **kwargs):
        
        form_instance=SignupForm()
        
        return render(request,"register.html",{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        
        form_instance=SignupForm(request.POST)
        
        if form_instance.is_valid():
            
            form_instance.save()
            
            # data=form_instance.cleaned_data
            
            # User.objects.create_user(**data)
            
            return redirect("login")
        
        return render(request,"register.html",{"form":form_instance})
    
    
class LoginView(View):
    
    def get(self,request,*args, **kwargs):
        
        form_instance=SigninForm()
        
        return render(request,"login.html",{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        
        form_instance=SigninForm(request.POST)
        
        if  form_instance.is_valid():
            
            data=form_instance.cleaned_data
            
            uname=data.get("username")
            
            pwd=data.get("password")
            
            user_object=authenticate(request,username=uname,password=pwd)
            
            print(user_object)
            
            if user_object:
                
                login(request,user_object)
                
                print("session started")
                
                return redirect("index")
            
        print("failed to login ")
            
        return render(request,"login.html",{"form":form_instance})
    
    
class IndexView(View):
    
    def get(self,request,*args, **kwargs):
        
        qs=Product.objects.all()
        
        return render(request,"index.html",{"data":qs})
    
    
class ProductdetailView(View):
    
    def get(self,request,*args,**kwargs):
        
        
        id=kwargs.get("pk")
        
        qs=Product.objects.get(id=id)
        
        return render(request,"product_detail.html",{"data":qs})
    
    
class AddToCartView(View):
    
    
    
    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        product_obj=Product.objects.get(id=id)

        #basket_obj=Basket.objects.get(name=request.user)

        basket_obj=request.user.cart

        size_name=request.POST.get("size")

        size_obj=Size.objects.get(name=size_name)

        qty=request.POST.get("qty")

        
        BasketItem.objects.create(

            product_object=product_obj,

            basket_object=basket_obj,

            size_object=size_obj,
            
            quantity=qty
            
        )
        print("added to cart")

        return redirect("index")
    
        
class CartItermsView(View):
    
    
    def get(self,request,*args, **kwargs):
        
        qs=request.user.cart.cartitems.filter(is_order_placed=False)
        
        
        return render(request,"cart_list.html",{"data":qs})
    
class CartDestroyView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        BasketItem.objects.get(id=id).delete()
        
        return redirect("cart-summary")  

class SignOutView(View):
    
    
    def get(self,request,*args, **kwargs):
        
        logout(request)
        
        return redirect("login")
    
    
class CartUpdateQuantityView(View):
    
    def post(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        basket_item=BasketItem.objects.get(id=id)
        
        action=request.POST.get("action")
        
        print(action)
        
        if action=="increment":
            
            basket_item.quantity+=1
            
        else:
            
            basket_item.quantity-=1
            
        basket_item.save()
    
        return redirect("cart-summary")
    
    
    
class PlaceOrderView(View):
    
    def get(self,request,*args, **kwargs):
        
        return render(request,"place_order.html")
    
    
    def post(self,request,*args, **kwargs):
        
        email=request.POST.get("email")
        
        phone=request.POST.get("phone")
        
        address=request.POST.get("address")
        
        payment_mode=request.POST.get("payment_mode")
        
        pin=request.POST.get("pin")
        
        user_obj=request.user
        
        cart_item_objects=request.user.cart.cartitems.filter(is_order_placed=False)
        
        if payment_mode == "cod":
            
            order_obj=Order.objects.create(

                user_object= user_obj,
                
                delivery_address= address,
                
                phone=phone,
                
                pin=pin,
                
                email=email,
                
                payment_mode=payment_mode, 
                
            )
            
            for bi in cart_item_objects:
                
                order_obj.basket_item_objects.add(bi)
                
                bi.is_order_placed=True
                
                bi.save()
                
            order_obj.save()
            
            
        
        print(email,phone,address,payment_mode,pin)
        
        
        return redirect("index")
    
    
    
class OrderSummaryView(View):
    
    def get(self,request,*args, **kwargs):
        
        
        qs=Order.objects.filter(user_object=request.user).order_by("created_date")
        
        
        
        return render(request,"order_summary.html",{"data":qs})
    
     
    
        